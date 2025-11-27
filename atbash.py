def atbash(text):
    result = ""
    for char in text:
        if char.isalpha():
            if char.islower():
                result += chr(219 - ord(char))
            else:
                result += chr(165 - ord(char))
        else:
            result += char
    return result

