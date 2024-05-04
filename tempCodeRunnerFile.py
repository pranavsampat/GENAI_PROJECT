if language == 'en':
        if "open google" in intent:
            subprocess.Popen(["C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"])
            return "Opening Google Chrome..."
        elif "show me images" in intent:
            return "Showing images..."
        elif "how are you" in intent:
            return "I'm fine, thank you!"
        elif "tell me a joke" in intent:
            return pyjokes.get_joke()
        elif "news" in intent:
            news = get_news()
            return f"Here are the latest news headlines: {news}"
        elif 'code' or 'what is' or 'how to' in intent:
            return ask_code(intent)
        # elif "what is" in intent:  # Check if user asked for arithmetic operation
        #     # Use regular expression to extract arithmetic expression
        #     match = re.search(r'(\d+)\s*\+\s*(\d+)', intent)
        #     if match:
        #         num1 = int(match.group(1))
        #         num2 = int(match.group(2))
        #         result = num1 + num2
        #         return f"The result of {num1} + {num2} is {result}."
        #     else:
        #         return "Sorry, I couldn't understand the arithmetic expression."
        elif "how much is" in intent:  
            match = re.search(r'how much is\s*(.*)', intent)
            if match:
                expression = match.group(1)
                expression = expression.replace("x", "*").replace("÷", "/").replace("-", "-")
                result = calculate_expression(expression)
                if result is not None:
                    return f"The result of {expression} is {result}."
                else:
                    return "Sorry, I couldn't calculate the expression."
            else:
                return "Sorry, I couldn't understand the expression."
        elif "play" in intent and "YouTube" in intent.lower():
            search_query = intent.replace("play", "").replace("YouTube", "")
    