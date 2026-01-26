# Comprehensive fix for complete_foundry_request
import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the function and replace it entirely with correct indentation
pattern = r'(async def complete_foundry_request\(request_body\):)\s*"""Complete.*?""".*?try:.*?except Exception as e:.*?raise e'

replacement = '''async def complete_foundry_request(request_body):
    """Complete a Foundry agent request and format the response."""
    try:
        foundry_response = await send_foundry_request(request_body)
        
        logging.debug(f"Raw Foundry response keys: {foundry_response.keys() if isinstance(foundry_response, dict) else 'not a dict'}")
        
        # Extract the response message from Foundry
        response_text = None
        
        # Foundry Responses API structure:
        # response = {
        #   "output": [
        #     {"type": "mcp_list_tools", ...},
        #     {"type": "mcp_call", ...},
        #     {"type": "file_search_call", ...},
        #     {"type": "message", "content": [{"type": "output_text", "text": "..."}]}
        #   ]
        # }
        
        if isinstance(foundry_response, dict) and "output" in foundry_response:
            output_list = foundry_response["output"]
            if isinstance(output_list, list):
                # Find the message object in the output list
                for item in output_list:
                    if isinstance(item, dict) and item.get("type") == "message":
                        content = item.get("content", [])
                        if isinstance(content, list) and len(content) > 0:
                            # Get the text from the first content item
                            first_content = content[0]
                            if isinstance(first_content, dict):
                                response_text = first_content.get("text")
                                if response_text:
                                    break
        
        # Fallback paths for other possible structures
        if not response_text:
            if isinstance(foundry_response, dict):
                # Try other possible paths
                if "choices" in foundry_response and len(foundry_response["choices"]) > 0:
                    choice = foundry_response["choices"][0]
                    if "message" in choice and "content" in choice["message"]:
                        response_text = choice["message"]["content"]
                elif "response" in foundry_response:
                    response_text = foundry_response["response"]
                elif "message" in foundry_response:
                    response_text = foundry_response["message"]
                elif "content" in foundry_response:
                    response_text = foundry_response["content"]
        
        if not response_text:
            # Final fallback: convert entire response to string
            response_text = json.dumps(foundry_response, ensure_ascii=False, indent=2)
            logging.warning(f"Could not extract text from Foundry response, using full JSON")
        
        logging.info(f"Extracted response text ({len(response_text)} chars): {response_text[:100]}...")
        
        # Format the response to match the expected structure
        history_metadata = request_body.get("history_metadata", {})
        
        formatted_response = {
            "id": str(uuid.uuid4()),
            "model": "foundry-agent",
            "created": int(time.time()),
            "object": "chat.completion",
            "choices": [
                {
                    "messages": [
                        {
                            "role": "assistant",
                            "content": response_text,
                        }
                    ],
                    "index": 0,
                    "finish_reason": "stop",
                }
            ],
            "history_metadata": history_metadata,
        }
        
        return formatted_response
        
    except Exception as e:
        logging.exception("Exception in complete_foundry_request")
        raise e'''

# Use DOTALL to match across lines
new_content = re.sub(pattern, replacement, content, count=1, flags=re.DOTALL)

if new_content == content:
    print("Warning: Pattern not found, trying alternative approach")
    # Find the function start
    func_start = content.find('async def complete_foundry_request(request_body):')
    if func_start != -1:
        # Find the next function definition
        next_func = content.find('\nasync def ', func_start + 10)
        if next_func == -1:
            next_func = content.find('\ndef ', func_start + 10)
        
        if next_func != -1:
            # Replace everything between
            new_content = content[:func_start] + replacement + '\n\n' + content[next_func:]
        else:
            print("Could not find next function")
    else:
        print("Could not find complete_foundry_request function")
else:
    print("Function replaced successfully")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Complete fix applied")
