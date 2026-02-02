from openai import OpenAI
import json
from core.config import settings 
from tools.StudentTool import get_student,add_student


conversation=[{"role":"system","content":"u are a admin of university system user is the admin worker for university"}]
client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = settings.nvidia_key
)
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_students",
            "description": "get all student",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_students",
            "description": "add student",
            "parameters": { 
                "type": "object",
                "properties": {
                    "student_name": {
                        "type": "string",
                        "description": "The full name of the student"
                    }
                },
                "required": ["student_name"]
            }
        },
    },
]

async def ask(message, role="user"):
    global conversation
    conversation.append({"role": role, "content": message})
    
    
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=conversation,
        tools=tools,
        
    )
    
    assistant_msg = completion.choices[0].message
    conversation.append(assistant_msg)

    if assistant_msg.tool_calls:
        tool_call = assistant_msg.tool_calls[0]
        
        if tool_call.function.name == "get_students":
            result = get_student()
            
            conversation.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": "get_students",
                "content": result
            })
            
            second_completion = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=conversation
            )
            final_resp = second_completion.choices[0].message.content
            conversation.append({"role": "assistant", "content": final_resp})
            return final_resp
        if(tool_call.function.name =="add_students") :
            
            args = json.loads(tool_call.function.arguments)
            print(args)
            name = args.get("student_name")
            res=add_student(name)
            conversation.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": "get_students",
                "content": res
            })
            second_completion = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=conversation
            )
            final_resp = second_completion.choices[0].message.content
            conversation.append({"role": "assistant", "content": final_resp})
            return final_resp

    return assistant_msg.content
