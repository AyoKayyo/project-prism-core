"""
Plugin Loader - Riley v2.0
Dynamic plugin system for extensible skills
"""
import importlib
import os
from pathlib import Path


class PluginLoader:
    """
    Loads and manages plugins from the plugins/ directory.
    Each plugin should have a register() function that returns a skill dict.
    """
    
    def __init__(self, plugin_dir="plugins"):
        self.plugin_dir = Path(plugin_dir)
        self.plugins = []
        print(f"🔌 [Plugins] Loader initialized")
    
    def load_plugins(self):
        """
        Scans plugin directory and loads all valid plugins.
        
        Returns: list of plugin dictionaries
        """
        if not self.plugin_dir.exists():
            print(f"⚠️ [Plugins] Directory not found: {self.plugin_dir}")
            return []
        
        plugins = []
        
        for file in self.plugin_dir.glob("*.py"):
            if file.name.startswith("_") or file.name == "__pycache__":
                continue
            
            try:
                # Import module
                module_name = file.stem
                spec = importlib.util.spec_from_file_location(module_name, file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Check for register function
                if hasattr(module, "register"):
                    plugin = module.register()
                    plugins.append(plugin)
                    print(f"✅ [Plugins] Loaded: {plugin.get('name', module_name)}")
                else:
                    print(f"⚠️ [Plugins] No register() in {module_name}")
            
            except Exception as e:
                print(f"❌ [Plugins] Failed to load {file.name}: {e}")
        
        self.plugins = plugins
        return plugins
    
    def execute_plugin(self, plugin_name, context=None):
        """
        Executes a specific plugin by name.
        
        Args:
            plugin_name: str - Name of the plugin
            context: dict - Context to pass to plugin (user message, etc.)
        
        Returns: Plugin execution result
        """
        for plugin in self.plugins:
            if plugin.get("name") == plugin_name:
                try:
                    return plugin["execute"](context)
                except Exception as e:
                    return f"Plugin error: {e}"
        
        return f"Plugin not found: {plugin_name}"
    
    def check_triggers(self, context):
        """
        Checks all plugins for trigger conditions and executes matching ones.
        
        Args:
            context: dict - Current context (user_message, etc.)
        
        Returns: list of (plugin_name, result) tuples
        """
        results = []
        
        for plugin in self.plugins:
            if "trigger" in plugin:
                try:
                    if plugin["trigger"](context):
                        result = plugin["execute"](context)
                        results.append((plugin["name"], result))
                except Exception as e:
                    print(f"⚠️ [Plugins] Trigger error in {plugin['name']}: {e}")
        
        return results


if __name__ == "__main__":
    # Test plugin loader
    print("🧪 Testing Plugin Loader\n")
    
    loader = PluginLoader()
    
    # Create example plugin directory if it doesn't exist
    Path("plugins").mkdir(exist_ok=True)
    
    # Create a sample plugin
    sample_plugin = '''
def register():
    """Example weather skill"""
    return {
        "name": "Weather Check",
        "description": "Checks the weather (mock)",
        "trigger": lambda ctx: "weather" in ctx.get("user_message", "").lower(),
        "execute": lambda ctx: "It's sunny! ☀️"
    }
'''
    
    with open("plugins/example_weather.py", "w") as f:
        f.write(sample_plugin)
    
    # Load plugins
    plugins = loader.load_plugins()
    print(f"\nLoaded {len(plugins)} plugins")
    
    # Test trigger
    results = loader.check_triggers({"user_message": "What's the weather?"})
    print(f"\nTrigger results: {results}")
