
from api.models import Character,Scene,Message
from typing import List, Dict, Optional
class DialogueControl:
   @staticmethod
   def build_prompt(
           character: Character,
           scene: Scene,
           message_history: Optional[List[Message]] = None
   ) -> Dict:
       """
       Build dialogue prompt

       Args:
           character: Character info
           scene: Scene info
           message_history: History of messages, defaults to None

       Returns:
           Dict: Processed prompt info
       """
       # Build character info
       character_info = (
           f"The role you play is {character.name}\n"
           f"Background Information: {character.background}\n"
           f"personality: {character.personality}"
       )

       # Build scene context
       context = (
           f"scene: {scene.description}\n"
           f"vibe: {scene.mood if scene.mood else 'normal'}"
       )

       # Process message history with defaults
       messages = []
       if message_history:
           for msg in message_history:
               messages.append({
                   "role": msg.role,
                   "content": msg.content
               })

       return {
           "character_info": character_info,
           "context": context,
           "messages": messages
       }