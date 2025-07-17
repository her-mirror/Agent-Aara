from typing import Dict, Any, List, Optional
import json
import os
import yaml
from dataclasses import dataclass

@dataclass
class Product:
    name: str
    description: str
    category: str
    subcategory: str
    price_range: str
    affiliate_link: str
    keywords: List[str]
    recommended_for: List[str]
    why_recommended: str

class ProductSuggestionTool:
    def __init__(self):
        self.products = self._load_product_database()
    
    def _load_product_database(self) -> List[Product]:
        """Load product database from YAML configuration file."""
        try:
            # Get the config path
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 
                'config', 
                'affiliate_links.yaml'
            )
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            products = []
            
            # Parse products from YAML structure
            products_data = config.get('products', {})
            
            for category, subcategories in products_data.items():
                for subcategory, items in subcategories.items():
                    for item in items:
                        product = Product(
                            name=item['name'],
                            description=item['description'],
                            category=category,
                            subcategory=subcategory,
                            price_range=item['price_range'],
                            affiliate_link=item['affiliate_link'],
                            keywords=item['keywords'],
                            recommended_for=item['recommended_for'],
                            why_recommended=item['why_recommended']
                        )
                        products.append(product)
            
            return products
            
        except Exception as e:
            print(f"Error loading affiliate config: {e}")
            # Fallback to minimal hardcoded products
            return [
                Product(
                    name="Basic Cleanser",
                    description="Gentle cleanser for all skin types",
                    category="skincare",
                    subcategory="cleanser",
                    price_range="$10-15",
                    affiliate_link="https://example.com/affiliate/cleanser",
                    keywords=["cleanser", "gentle"],
                    recommended_for=["all_skin_types"],
                    why_recommended="Suitable for daily use"
                )
            ]
    
    def analyze_conversation_context(self, user_input: str, chat_history: List[Dict[str, str]]) -> Dict[str, Any]:
        """Analyze the conversation to extract context for product suggestions."""
        user_input_lower = user_input.lower()
        
        context = {
            'skin_type': '',
            'skin_concerns': [],
            'health_concerns': [],
            'mentioned_products': [],
            'budget_indicators': [],
            'age_mentioned': False,
            'lifestyle_factors': []
        }
        
        # Extract from current user input
        # Skin type detection
        skin_types = ['oily', 'dry', 'combination', 'sensitive', 'normal', 'acne-prone']
        for skin_type in skin_types:
            if skin_type in user_input_lower:
                context['skin_type'] = skin_type
                break
        
        # Skin concerns from current input
        skin_concerns = ['acne', 'wrinkles', 'fine lines', 'dark spots', 'blackheads', 'enlarged pores', 'redness', 'dryness', 'oiliness', 'sensitivity']
        for concern in skin_concerns:
            if concern in user_input_lower:
                context['skin_concerns'].append(concern.replace(' ', '_'))
        
        # Extract health concerns
        health_concerns = ['pcos', 'irregular periods', 'heavy periods', 'cramps', 'pms', 'iron deficiency', 'fatigue', 'hormonal imbalance']
        for concern in health_concerns:
            if concern in user_input_lower:
                context['health_concerns'].append(concern.replace(' ', '_'))
        
        # ENHANCED: Analyze chat history for additional context (INCLUDING ARA'S RESPONSES)
        for exchange in chat_history[-5:]:  # Look at last 5 exchanges
            
            # Extract from user messages
            if 'user' in exchange and exchange['user']:
                user_msg = exchange['user'].lower()
                
                # Look for skin type mentions
                for skin_type in skin_types:
                    if skin_type in user_msg and not context['skin_type']:
                        context['skin_type'] = skin_type
                
                # Look for product mentions
                product_keywords = ['cleanser', 'moisturizer', 'serum', 'sunscreen', 'supplement', 'vitamin', 'toner', 'exfoliant']
                for keyword in product_keywords:
                    if keyword in user_msg and keyword not in context['mentioned_products']:
                        context['mentioned_products'].append(keyword)
                
                # Look for budget indicators
                budget_keywords = ['affordable', 'cheap', 'expensive', 'budget', 'drugstore', 'high-end']
                for keyword in budget_keywords:
                    if keyword in user_msg and keyword not in context['budget_indicators']:
                        context['budget_indicators'].append(keyword)
            
            # ENHANCED: Extract from Ara's responses (this is the key fix!)
            if 'ara' in exchange and exchange['ara']:
                ara_msg = exchange['ara'].lower()
                ara_msg_original = exchange['ara']  # Keep original for debugging
                
                print(f"📋 ANALYZING ARA'S RESPONSE: {ara_msg_original[:100]}...")
                
                # Look for skin type determinations in Ara's responses
                skin_type_patterns = [
                    'your skin type is',
                    'skin type is',
                    'sounds like your skin type is',
                    'it sounds like your skin type is',
                    'determined skin type',
                    'skin type: combination',
                    'skin type: oily',
                    'skin type: dry',
                    'skin type: sensitive',
                    'skin type: normal'
                ]
                
                for pattern in skin_type_patterns:
                    if pattern in ara_msg:
                        print(f"📋 FOUND PATTERN: '{pattern}' in message")
                        
                        # Extract the skin type that follows the pattern with better handling
                        pattern_start = ara_msg.find(pattern) + len(pattern)
                        text_after_pattern = ara_msg[pattern_start:pattern_start + 100]
                        print(f"📋 TEXT AFTER PATTERN: '{text_after_pattern}'")
                        
                        # Look for skin types, handling markdown and variations
                        for skin_type in skin_types:
                            # Check for the skin type in various formats
                            skin_type_variations = [
                                skin_type,
                                f"**{skin_type}**",
                                f"*{skin_type}*",
                                skin_type.title(),
                                f"**{skin_type.title()}**",
                                f"*{skin_type.title()}*"
                            ]
                            
                            for variation in skin_type_variations:
                                if variation.lower() in text_after_pattern:
                                    if not context['skin_type']:  # Only set if not already found
                                        context['skin_type'] = skin_type
                                        print(f"📋 ✅ EXTRACTED SKIN TYPE: {skin_type} (found as '{variation}')")
                                    break
                            
                            if context['skin_type']:  # Break outer loop if found
                                break
                        
                        if context['skin_type']:  # Break pattern loop if found
                            break
                
                # If no pattern matched, try a more aggressive search
                if not context['skin_type']:
                    print(f"📋 NO PATTERN MATCHED - TRYING AGGRESSIVE SEARCH")
                    
                    # Look for skin types mentioned anywhere with markdown
                    for skin_type in skin_types:
                        aggressive_patterns = [
                            f"**{skin_type}**",
                            f"*{skin_type}*", 
                            f"**{skin_type.title()}**",
                            f"*{skin_type.title()}*",
                            skin_type,
                            skin_type.title()
                        ]
                        
                        for pattern in aggressive_patterns:
                            if pattern.lower() in ara_msg:
                                context['skin_type'] = skin_type
                                print(f"📋 ✅ AGGRESSIVE MATCH FOUND: {skin_type} (pattern: '{pattern}')")
                                break
                        
                        if context['skin_type']:
                            break
                
                # Extract skin concerns mentioned in Ara's analysis
                concern_patterns = [
                    'breakouts in the t-zone',
                    'shiny primarily in the t-zone',
                    'comfortable and balanced',
                    'normal-sized pores',
                    'tolerates new products'
                ]
                
                for pattern in concern_patterns:
                    if pattern in ara_msg:
                        if 't-zone' in pattern and 'combination_tzone' not in context['skin_concerns']:
                            context['skin_concerns'].append('combination_tzone')
                        elif 'balanced' in pattern and 'balanced_skin' not in context['skin_concerns']:
                            context['skin_concerns'].append('balanced_skin')
                
                # Look for routine recommendations in Ara's responses to understand needs
                routine_keywords = ['morning routine', 'evening routine', 'gentle cleanser', 'lightweight moisturizer', 'oil-free', 'broad-spectrum spf']
                for keyword in routine_keywords:
                    if keyword in ara_msg and keyword.replace(' ', '_') not in context['mentioned_products']:
                        context['mentioned_products'].append(keyword.replace(' ', '_'))
        
        print(f"📋 FINAL EXTRACTED CONTEXT:")
        print(f"  Skin Type: {context['skin_type']}")
        print(f"  Skin Concerns: {context['skin_concerns']}")
        print(f"  Health Concerns: {context['health_concerns']}")
        print(f"  Mentioned Products: {context['mentioned_products']}")
        
        return context
    
    def get_relevant_products(self, context: Dict[str, Any], max_suggestions: int = 3) -> List[Product]:
        """Get relevant products based on conversation context."""
        relevant_products = []
        
        print(f"📋 SEARCHING FOR PRODUCTS:")
        print(f"  Target skin type: '{context['skin_type']}'")
        print(f"  Available products: {len(self.products)}")
        
        for product in self.products:
            relevance_score = 0
            
            print(f"📋 Checking product: {product.name}")
            print(f"  Recommended for: {product.recommended_for}")
            
            # Score based on skin type match
            if context['skin_type'] and context['skin_type'] in product.recommended_for:
                relevance_score += 3
                print(f"  ✅ SKIN TYPE MATCH! Score +3 (total: {relevance_score})")
            
            # Score based on skin concerns
            for concern in context['skin_concerns']:
                if concern in product.keywords or concern.replace('_', ' ') in product.keywords:
                    relevance_score += 2
                    print(f"  ✅ CONCERN MATCH: {concern} - Score +2 (total: {relevance_score})")
            
            # Score based on health concerns  
            for concern in context['health_concerns']:
                if concern in product.keywords or concern.replace('_', ' ') in product.keywords:
                    relevance_score += 2
                    print(f"  ✅ HEALTH CONCERN MATCH: {concern} - Score +2 (total: {relevance_score})")
            
            # Score based on mentioned products
            for mentioned in context['mentioned_products']:
                if mentioned in product.subcategory or mentioned in product.keywords:
                    relevance_score += 1
                    print(f"  ✅ MENTIONED PRODUCT MATCH: {mentioned} - Score +1 (total: {relevance_score})")
            
            if relevance_score > 0:
                relevant_products.append((product, relevance_score))
                print(f"  ✅ PRODUCT ADDED with score: {relevance_score}")
            else:
                print(f"  ❌ PRODUCT SKIPPED (score: 0)")
        
        # Sort by relevance score and return top suggestions
        relevant_products.sort(key=lambda x: x[1], reverse=True)
        print(f"📋 FOUND {len(relevant_products)} RELEVANT PRODUCTS")
        
        return [product for product, score in relevant_products[:max_suggestions]]
    
    def format_product_suggestions(self, products: List[Product], context: Dict[str, Any]) -> str:
        """Format product suggestions into a natural response."""
        if not products:
            return ""
        
        suggestions = "\n\n**💡 Product Suggestions Based on Our Conversation:**\n\n"
        
        for i, product in enumerate(products, 1):
            suggestions += f"**{i}. {product.name}** ({product.price_range})\n"
            suggestions += f"*{product.description}*\n"
            suggestions += f"**Why I recommend this:** {product.why_recommended}\n"
            suggestions += f"[Shop Here 🛒]({product.affiliate_link})\n\n"
        
        # Add disclaimer from config
        try:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 
                'config', 
                'affiliate_links.yaml'
            )
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            disclaimer = config.get('affiliate_settings', {}).get('disclaimer_text', '')
            suggestions += f"*{disclaimer}*"
        except:
            suggestions += "*Please note: These are affiliate links. I may earn a small commission if you purchase through these links, at no extra cost to you. Always patch test new skincare products and consult healthcare providers for supplements.*"
        
        return suggestions

def product_suggestion_tool(state: Dict[str, Any]) -> Dict[str, Any]:
    """Tool that analyzes conversation and suggests relevant products with affiliate links."""
    
    # Check if product suggestions are appropriate for this conversation
    user_input = state['user_input'].lower()
    chat_history = state.get('chat_history', [])
    
    # Don't suggest products for emergencies or crisis situations
    emergency_keywords = ['emergency', 'crisis', 'severe pain', 'heavy bleeding', 'suicide', 'self harm']
    if any(keyword in user_input for keyword in emergency_keywords):
        return state
    
    # Don't suggest products if user explicitly asks not to
    if any(phrase in user_input for phrase in ['no products', 'no recommendations', 'no shopping']):
        return state
    
    tool = ProductSuggestionTool()
    
    # Analyze conversation context
    context = tool.analyze_conversation_context(user_input, chat_history)
    
    # ENHANCED: Check if we have sufficient context for recommendations
    has_context = (context['skin_type'] or context['skin_concerns'] or 
                   context['health_concerns'] or context['mentioned_products'])
    
    if has_context:
        print(f"📋 SUFFICIENT CONTEXT FOUND - PROVIDING RECOMMENDATIONS")
        
        # Get relevant products
        relevant_products = tool.get_relevant_products(context, max_suggestions=3)
        
        if relevant_products:
            # Create a personalized response based on context
            response_intro = "Based on our conversation"
            
            if context['skin_type']:
                response_intro += f" and your **{context['skin_type']} skin type**"
            
            if context['skin_concerns']:
                concerns_text = ", ".join([concern.replace('_', ' ') for concern in context['skin_concerns']])
                response_intro += f" and concerns about {concerns_text}"
                
            response_intro += ", here are my personalized product recommendations:\n\n"
            
            # Format suggestions with personalized intro
            product_suggestions = response_intro + tool.format_product_suggestions(relevant_products, context)
            
            # Add to existing response or create new one
            if state.get('final_response'):
                state['final_response'] += "\n\n" + product_suggestions
            else:
                state['final_response'] = product_suggestions
            
            # Log what we suggested
            state['intermediate_steps'].append({
                'tool_used': 'product_suggestion',
                'context': context,
                'products_suggested': [p.name for p in relevant_products],
                'suggestion_reason': 'conversation_context_match'
            })
        else:
            # Have context but no matching products
            response = f"I understand you're looking for product recommendations"
            if context['skin_type']:
                response += f" for your {context['skin_type']} skin"
            response += ". While I don't have specific products in my current database that perfectly match your needs, I'd recommend:\n\n"
            response += "- Consulting with a dermatologist for personalized recommendations\n"
            response += "- Looking for products with ingredients I mentioned in our conversation\n" 
            response += "- Checking reviews from people with similar skin types and concerns\n\n"
            response += "Would you like me to provide more specific ingredient recommendations or skincare routine advice instead?"
            
            state['final_response'] = response
    else:
        print(f"📋 INSUFFICIENT CONTEXT - ASKING FOR CLARIFICATION")
        
        # Provide helpful guidance for getting better recommendations
        response = "I'd love to suggest personalized products for you! To provide the best recommendations, could you please tell me:\n\n"
        response += "**About your skin:**\n"
        response += "- What's your skin type? (oily, dry, combination, sensitive, or normal)\n"
        response += "- Any specific concerns? (acne, dryness, aging, sensitivity, etc.)\n"
        response += "- What products are you currently using?\n\n"
        response += "**About your needs:**\n"
        response += "- What type of products are you looking for? (cleanser, moisturizer, serum, etc.)\n"
        response += "- Any budget preferences?\n"
        response += "- Any ingredients you love or want to avoid?\n\n"
        response += "The more specific you are, the better I can tailor my recommendations to your unique needs! 💫"
        
        state['final_response'] = response
    
    return state 