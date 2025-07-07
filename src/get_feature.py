import openai
import base64
import os
import cv2
import re
import matplotlib.pyplot as plt


class ImageChatBot:
    def __init__(self):
        openai.api_key = os.environ["OPENAI_API_KEY"]
        
    
    def prepare_image_list(self, image_path: str) -> list:
        image_list = []
        for image_path in [image_path]:
            image = cv2.imread(image_path)
            # resized_image = cv2.resize(image, (width, height))
            # cv2.imwrite(output_path + str(n) + '.jpg', resized_image)
            # image_list.append(output_path + str(n) + '.jpg')
            image_list.append(image_path)

            # n = n + 1
            return image_list
        

    def encode_image(self):
        self.base64_image_list = []
        for image_path in (self.image_list):
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
                self.base64_image_list.append(base64_image)
        return  

    def set_inital_prompt(self) -> None:
        self.messages = [
            {"role": "system", "content": "You are a great assistant who can analyze a human featre image."},
            {"role": "system", "content": "I send you an image of included person and you must analyze the image and return the feature of the person."},
            {"role": "system", "content": "Find the characteristics of the person from the following list:[hat, pants, shoes, hair color, whether they wear glasses, etc]."},
            {"role": "system", "content": "You must return the feature of the person in the image as a list of strings."},
            {"role": "system", "content": "Let's think step by step."},
            
            
        
            #対話例
            {"role": "system", "content": "Following is an example of talk between a user and an assistant."},
            {"role": "user", "content": "Please tell me the 4 features of the person in the image."},
            {"role": "assistant", "content": "['has a short black hair.', 'wearing a blue shirt', 'wearing glasses', 'wearing green pants']"},
        ]


    def create_chat(self, image_path: str) -> str:
        """        Create a chat with the image and return the response content.  
        Args:
            image_path (str): The path to the image file. 
        Returns:
            str: The response content from the chat.
        """
        self.image_list = self.prepare_image_list(image_path)
        self.encode_image()
        self.set_inital_prompt()
      
        self.messages.append(
            {"role": "user","content":
               [
                    {"type": "text", "text": "Please tell me the 4 features of the person in the image."},
                    {"type": "image_url","image_url": {"url":  f"data:image/jpeg;base64,{self.base64_image_list[0]}",},
                    },
                ],
            },
        )

        response = openai.chat.completions.create(
            model="chatgpt-4o-latest",
            messages=self.messages,
            temperature=0,
        )

        
        return response.choices[0].message.content

 
if __name__ == "__main__":
    # image_path = "./fig/image_2024-07-05 18_23_03.797964.jpg"
    image_path = "./fig/image_2025-04-30 13_06_31.878916.jpg"
    chat_bot = ImageChatBot()
    response_content = chat_bot.create_chat(image_path)
    print(response_content)
else:
    print("This script is not intended to be imported as a module.")

   