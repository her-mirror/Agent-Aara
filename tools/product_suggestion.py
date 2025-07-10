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
        """Analyze conversation to extract product suggestion context."""
        context = {
            'skin_type': None,
            'skin_concerns': [],
            'health_concerns': [],
            'mentioned_products': [],
            'lifestyle_factors': [],
            'budget_indicators': [],
            'urgency_level': 'low'
        }
        
        # Analyze current input
        user_input_lower = user_input.lower()
        
        # Extract skin type
        skin_types = ['oily', 'dry', 'combination', 'sensitive', 'acne-prone', 'mature']
        for skin_type in skin_types:
            if skin_type.replace('-', ' ') in user_input_lower or skin_type.replace('-', '') in user_input_lower:
                context['skin_type'] = skin_type.replace('-', '_')
                
        # Extract skin concerns
        skin_concerns = ['acne', 'wrinkles', 'dark spots', 'hyperpigmentation', 'redness', 'dryness', 'oiliness', 'sensitivity', 'aging', 'pores']
        for concern in skin_concerns:
            if concern in user_input_lower:
                context['skin_concerns'].append(concern)
        
        # Extract health concerns
        health_concerns = ['pcos', 'irregular periods', 'heavy periods', 'cramps', 'pms', 'iron deficiency', 'fatigue', 'hormonal imbalance']
        for concern in health_concerns:
            if concern in user_input_lower:
                context['health_concerns'].append(concern.replace(' ', '_'))
        
        # Analyze chat history for additional context
        for exchange in chat_history[-3:]:  # Look at last 3 exchanges
            if 'user' in exchange:
                msg = exchange['user'].lower()
                
                # Look for product mentions
                product_keywords = ['cleanser', 'moisturizer', 'serum', 'sunscreen', 'supplement', 'vitamin']
                for keyword in product_keywords:
                    if keyword in msg:
                        context['mentioned_products'].append(keyword)
                
                # Look for budget indicators
                budget_keywords = ['affordable', 'cheap', 'expensive', 'budget', 'drugstore', 'high-end']
                for keyword in budget_keywords:
                    if keyword in msg:
                        context['budget_indicators'].append(keyword)
        
        return context
    
    def get_relevant_products(self, context: Dict[str, Any], max_suggestions: int = 3) -> List[Product]:
        """Get relevant products based on conversation context."""
        relevant_products = []
        
        for product in self.products:
            relevance_score = 0
            
            # Score based on skin type match
            if context['skin_type'] and context['skin_type'] in product.recommended_for:
                relevance_score += 3
            
            # Score based on skin concerns
            for concern in context['skin_concerns']:
                if concern in product.keywords or concern.replace('_', ' ') in product.keywords:
                    relevance_score += 2
            
            # Score based on health concerns  
            for concern in context['health_concerns']:
                if concern in product.keywords or concern.replace('_', ' ') in product.keywords:
                    relevance_score += 2
            
            # Score based on mentioned products
            for mentioned in context['mentioned_products']:
                if mentioned in product.subcategory or mentioned in product.keywords:
                    relevance_score += 1
            
            if relevance_score > 0:
                relevant_products.append((product, relevance_score))
        
        # Sort by relevance score and return top suggestions
        relevant_products.sort(key=lambda x: x[1], reverse=True)
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
    
    # Only suggest products if there's relevant context
    if (context['skin_concerns'] or context['health_concerns'] or 
        context['skin_type'] or context['mentioned_products']):
        
        # Get relevant products
        relevant_products = tool.get_relevant_products(context, max_suggestions=2)
        
        if relevant_products:
            # Format suggestions
            product_suggestions = tool.format_product_suggestions(relevant_products, context)
            
            # Add to existing response or create new one
            if state.get('final_response'):
                state['final_response'] += product_suggestions
            else:
                state['final_response'] = product_suggestions
            
            # Log what we suggested
            state['intermediate_steps'].append({
                'tool_used': 'product_suggestion',
                'context': context,
                'products_suggested': [p.name for p in relevant_products],
                'suggestion_reason': 'conversation_context_match'
            })
    
    return state 