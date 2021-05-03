import random
class Region():
  def __init__(self):
    self.region={"ể":"ễ","ễ":"ể","ẳ":"ẵ","ẵ":"ẳ","ẩ":"ẫ","ẫ":"ẩ","ử":"ữ","ữ":"ử","ổ":"ỗ","ỗ":"ổ","ở":"ỡ","ỡ":"ở","ẻ":"ẽ","ẽ":"ẻ","ũ":"ủ","ủ":"ũ","ã":"ả","ả":"ã","ỏ":"õ","õ":"ỏ","s":"x","l":"n","n":"l","x":"s","d":"g","S":"X","L":"N","N":"L","X":"S","Gi":"D","D":"G", "uộc": "ục", "ục":"uộc", "ch": "tr", "tr": "ch", "k": "c", "c": "k", "i": "y", "y": "i", "ngh":"ng", "ng": "ngh", "gi": "d", "Tr": "Ch", "Ch": "Tr", "Ngh": "Ng", "Ng": "Ngh", "C": "K", "K": "C", "gh": "g"}
    self.region_vowel = {"ể":"ễ","ễ":"ể","ẳ":"ẵ","ẵ":"ẳ","ẩ":"ẫ","ẫ":"ẩ","ử":"ữ","ữ":"ử","ổ":"ỗ","ỗ":"ổ","ở":"ỡ","ỡ":"ở","ẻ":"ẽ", "ẽ":"ẻ","ũ":"ủ","ủ":"ũ","ã":"ả","ả":"ã","ỏ":"õ","õ":"ỏ"}
    self.region_consonant = {"s":"x","l":"n","n":"l","x":"s","d":"gi","S":"X","L":"N","N":"L","X":"S","Gi":"D","D":"Gi"}
    self.special_case = {"ng_end": "n", "n_end_g": "n", "nh_end": "n", "n_end_h": "nh", "d_" : "gi", "D_":"Gi"}
      
  def generate(self,token):
    possible_error = []

    if token is None or token == "" or token == " ":
      return False
    
    if len(token) > 1:
      try:
        if token[0] == "d":
          if token[1] in "iíìỉĩị":  
            possible_error.append("d")
          else:
            possible_error.append("d_")
        elif token[0] == "D": 
          if token[1] in "iíìỉĩị":
            possible_error.append("D")
          else:
            possible_error.append("D_")
      except IndexError:
        pass

      #case: gi -> ghi / ghi -> gi
      if token[:2] == "gh":
        possible_error.append("gh")
      
      #case: gi->di / g -> d 

      #case: nganh - > nghanh / nghieng -> ngieng
      try:
        if token[:2] == "ng":
          if token[2] == "h":
            possible_error.append("ngh")
          else: 
            possible_error.append("ng")
        elif token[:2] == "Ng":
          if token[2] == "h":
            possible_error.append("Ngh")
          else:
            possible_error.append("Ng")
      except IndexError: 
        pass
      
      #case: nhung -> nhun / khoang -> khoan
      if token[-3:] in "ang¶áng¶àng¶ảng¶ãng¶ạng¶âng¶ấng¶ầng¶ẩng¶ẫng¶ậng¶ăng¶ắng¶ằng¶ẳng¶ẵng¶ặng":
        possible_error.append("ng_end")
      # if token[-1:] == "n": 
      #   possible_error.append("n_end_g")
        
      #case: nhanh -> nhan / nhan -> nhanh
      if token[-3:] in "anh¶ánh¶ành¶ảnh¶ãnh¶ạnh":
        possible_error.append("nh_end")
      # if token[-1:] == "n":
      #   possible_error.append("n_end_h")
      
      #case: rốt cuộc -> rốt cục
      if "uộc" in token and "qu" not in token:
        possible_error.append("uộc")
      elif "ục" in token and "qu" not in token and token[-1] != "c":
        possible_error.append("ục")

      #case ch - tr
      if token[:2] == "ch":
        possible_error.append("ch")
      elif token[:2] == "tr":
        possible_error.append("tr")
      elif token[:2] == "Ch":
        possible_error.append("Ch")
      elif token[:2] == "Tr":
        possible_error.append("Tr")

      #case k - c
      # if token[0] == "c" and token[1] != "h":
      #   possible_error.append("c")
      try:
        if token[0] == "k" and token[1] != "h":
          possible_error.append("k")
        # elif token[0] == "C" and token[1] != "h":
        #   possible_error.append("C")
        elif token[0] == "K" and token[1] != "h":
          possible_error.append("K")
      except IndexError:
        pass
      #case i - y
      # if token[-1] == "i":
      #   possible_error.append("i")
      # elif token[-1] == "y":
      #   possible_error.append("y")
      
      #case gi -> d:
      if token[:2] == "gi":
        possible_error.append("gi")
      elif token[:2] == "Gi":
        possible_error.append("Gi")
    else:
    #the left case: 
      for i in range(0, len(token)):
        if i == 0:
          try: 
            if token[0] in self.region_consonant and (token[1] != "g" and token[1] != "h"):
              possible_error.append(token[0])
              continue
          except IndexError:
            continue
        if token[i] in self.region_vowel:
          possible_error.append(token[i])
      
    # other_error = [i for i in token if i in self.region.keys()]
    # for error in other_error:
    #   possible_error.append(other_error)
    #possible_error = [i for i in token if i in self.region.keys()]
    
    if len(possible_error) > 0:
      # print("possible_error", possible_error)
      token_error = random.choice(possible_error)
      # print("token_choice", token_error)
      if token_error not in self.special_case:   
        return token.replace(token_error, self.region[token_error], 1)
      else: 
        if token_error == "ng_end":
          return token[:-1]
        elif token_error == "n_end_g":
          return token + "g"
        elif token_error == "nh_end":
          return token[:-1]
        elif token_error == "n_end_h":
          return token + "h"
        elif token_error == "d_":
          return "gi" + token[1:]
        elif token_error == "D_":
          return "Gi" + token[1:]
        return False
    else:
      return False

