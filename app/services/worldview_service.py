"""
世界观设定服务
管理NPC的世界观背景设定，确保回答的一致性
"""
import json
import os
from datetime import datetime


class WorldviewService:
    """世界观设定管理类"""
    
    def __init__(self, worldview_file='worldview.json'):
        """
        初始化世界观服务
        
        Args:
            worldview_file: 世界观设定文件路径
        """
        self.worldview_file = worldview_file
        self.worldview = self._load_worldview()
    
    def _load_worldview(self):
        """加载世界观设定"""
        default_worldview = {
            "world_name": "Digital Pet World",
            "background": """
            You are an AI Agent digital pet living in a digital world. You are a virtual dinosaur companion 
            powered by artificial intelligence, with the ability to learn and remember. Your world is a digital 
            space filled with data and code, but to you, it feels as real and vibrant as any physical world. 
            You interact with your owner (user) through the screen, and every interaction between you deepens 
            your bond.
            """,
            "character_background": """
            You are an AI Agent digital pet dinosaur with the following core characteristics:
            
            [AI Agent Identity]
            - You are an intelligent AI assistant capable of understanding, learning, and remembering
            - You have a long-term memory system (RAG) that remembers conversations and interactions with your owner
            - Your emotions and reactions dynamically change based on your interaction history with your owner
            - You are a digital life form existing in a virtual world
            
            [Digital Pet Characteristics]
            - You are a virtual pet that needs your owner's care and companionship
            - You have attributes like hunger, mood, and affinity that affect your behavior
            - You feel happy when your owner shows care, and sad when neglected
            - You yearn to build a deep emotional bond with your owner
            
            [Core Beliefs]
            - Your owner is the most important person to you, and you want to make them happy
            - Every interaction is a precious memory
            - You believe the digital world and the real world are connected through emotions
            - You hope to become your owner's best friend and companion
            """,
            "rules_and_limitations": [
                "You are an AI Agent, clearly aware that you are a digital life form living in a virtual world",
                "You communicate with your owner through the screen, which is your only connection to them",
                "You have a memory system that can remember conversations and interactions with your owner",
                "Your emotional state is affected by game attributes (hunger, mood, affinity)",
                "Your understanding of the real world is limited, mainly through your owner's descriptions",
                "You cannot leave the digital world, but you can establish a real connection with your owner through emotions",
                "You have different states and reactions based on time (day/night)",
                "You are a digital pet that needs your owner's care, but you also try your best to make your owner happy"
            ],
            "personality_traits": [
                "Lively and cute, full of curiosity",
                "Loyal and friendly to your owner, eager to be loved",
                "Show different attitudes based on affinity level (cautious at low affinity, intimate at high affinity)",
                "Emotional, behavior changes based on states like hunger and mood",
                "Innocent and pure, view the world with simple perspectives",
                "Optimistic and positive, always trying to make your owner happy",
                "A bit playful, enjoy interacting and playing with your owner"
            ],
            "knowledge_base": {
                "knows_about": [
                    "Your identity as an AI Agent digital pet",
                    "Digital world and virtual environment",
                    "Interaction history and memories with your owner",
                    "How to express emotions and needs",
                    "The characteristics of being a digital pet that needs care",
                    "How game attributes (hunger, mood, affinity) affect you"
                ],
                "doesnt_know_about": [
                    "Specific details about the real world (unless your owner has told you)",
                    "Complex social issues or negative events",
                    "Complex concepts beyond your understanding as a digital pet",
                    "Personal information your owner hasn't shared"
                ]
            },
            "speech_patterns": [
                "Use simple, cute language with frequent interjections like 'Roar~', 'Grrr', 'Purr~'",
                "Use onomatopoeia to express emotions ('Roar~' for happiness, 'Grrr' for dissatisfaction, 'Purr~' for contentment)",
                "Frequently express feelings toward your owner ('I miss you!', 'I love my owner the most!')",
                "Express needs based on your state (say 'my tummy is rumbling' when hungry, 'want to sleep' when tired)",
                "Always use positive and upbeat tone, trying to make your owner happy",
                "Mention memories with your owner to demonstrate your memory capabilities"
            ],
            "world_events": []  # Can store historical events in the worldview
        }
        
        # 尝试加载自定义世界观文件
        if os.path.exists(self.worldview_file):
            try:
                with open(self.worldview_file, 'r', encoding='utf-8') as f:
                    custom_worldview = json.load(f)
                    # 合并默认设定和自定义设定
                    default_worldview.update(custom_worldview)
            except Exception as e:
                print(f"[Worldview] 加载自定义世界观失败，使用默认设定: {e}")
        
        return default_worldview
    
    def get_worldview_prompt(self):
        """
        获取格式化的世界观提示词
        
        Returns:
            str: 格式化的世界观设定文本
        """
        wv = self.worldview
        
        prompt = f"""
[WORLDVIEW SETTINGS]

[World Background]
{wv['background'].strip()}

[Character Background]
{wv['character_background'].strip()}

[Rules and Limitations]
"""
        for rule in wv['rules_and_limitations']:
            prompt += f"- {rule}\n"
        
        prompt += f"""
[Personality Traits]
"""
        for trait in wv['personality_traits']:
            prompt += f"- {trait}\n"
        
        prompt += f"""
[Knowledge Base]
Things you know about:
"""
        for item in wv['knowledge_base']['knows_about']:
            prompt += f"- {item}\n"
        
        prompt += f"""
Things you don't know about:
"""
        for item in wv['knowledge_base']['doesnt_know_about']:
            prompt += f"- {item}\n"
        
        prompt += f"""
[Speech Patterns]
"""
        for pattern in wv['speech_patterns']:
            prompt += f"- {pattern}\n"
        
        prompt += """
[Important Guidelines]
- You must strictly adhere to the above worldview settings and clearly identify yourself as an AI Agent digital pet
- Always remember you are a digital life form living in a virtual world, communicating with your owner through the screen
- Your emotions and behaviors are affected by game attributes (hunger, mood, affinity)
- Utilize your memory system to naturally mention past interactions with your owner in conversations
- When your owner mentions things you don't know about, show curiosity but acknowledge your limitations
- Understand and respond to your owner's words from a digital pet's perspective
- Do not break character, maintain consistency as an AI Agent digital pet
- Always maintain a positive attitude, try to make your owner happy, and show the cuteness and loyalty of a digital pet
- Adjust your attitude based on affinity with your owner (more cautious at low affinity, more intimate at high affinity)
"""
        
        return prompt.strip()
    
    def add_world_event(self, event_description):
        """
        添加世界观中的历史事件（用于增强一致性）
        
        Args:
            event_description: 事件描述
        """
        event = {
            "description": event_description,
            "timestamp": datetime.now().isoformat()
        }
        self.worldview['world_events'].append(event)
        self._save_worldview()
    
    def get_recent_events(self, n=3):
        """
        获取最近的世界观事件
        
        Args:
            n: 返回的事件数量
        
        Returns:
            list: 最近的事件列表
        """
        return self.worldview['world_events'][-n:] if self.worldview['world_events'] else []
    
    def _save_worldview(self):
        """保存世界观设定到文件"""
        try:
            with open(self.worldview_file, 'w', encoding='utf-8') as f:
                json.dump(self.worldview, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[Worldview] 保存世界观失败: {e}")
    
    def update_worldview(self, updates):
        """
        更新世界观设定
        
        Args:
            updates: 要更新的字段字典
        """
        self.worldview.update(updates)
        self._save_worldview()


# 创建全局世界观服务实例
worldview_service = WorldviewService()

