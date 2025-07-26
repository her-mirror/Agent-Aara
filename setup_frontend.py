#!/usr/bin/env python3
"""
Setup script for creating the Next.js frontend files
"""
import os

def create_directory(path):
    """Create directory if it doesn't exist"""
    os.makedirs(path, exist_ok=True)
    print(f"Created directory: {path}")

def create_file(path, content):
    """Create file with content"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created file: {path}")

def main():
    """Main setup function"""
    print("Setting up Next.js frontend for Aara Health Agent...")
    
    # Create directories
    directories = [
        'frontend',
        'frontend/app',
        'frontend/components',
        'frontend/types',
        'frontend/lib',
        'frontend/public',
    ]
    
    for dir_path in directories:
        create_directory(dir_path)
    
    # Create PostCSS config
    postcss_config = """module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}"""
    
    create_file('frontend/postcss.config.js', postcss_config)
    
    # Create TypeScript config
    tsconfig = """{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "es6"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}"""
    
    create_file('frontend/tsconfig.json', tsconfig)
    
    print("Frontend setup complete!")

if __name__ == "__main__":
    main() 