import string 
import pandas as pd
# Open the file in read mode 

class wordFrequency:

    def __init__(self):
        pass
    
    def getWordFreq_toText(self,textFileName,csvFileName,col_list = ["text"]):

        textFile = open(textFileName , 'w',encoding="utf-8",newline="")
        df = pd.read_csv(csvFileName , usecols=col_list)

        # Create an empty dictionary 
        d = dict() 

        # Loop through each line of the file 
        for line in df['text']: 
            
            # Remove the leading spaces and newline character 
            line = line.strip() 
        
            # Convert the characters in line to  
            # lowercase to avoid case mismatch 
            line = line.lower() 
        
            # Remove the punctuation marks from the line 
            line = line.translate(line.maketrans("", "", string.punctuation)) 
        
            # Split the line into words 
            words = line.split(" ") 
        
            # Iterate over each word in line 
            for word in words: 
                # Check if the word is already in dictionary 
                if word in d: 
                    # Increment count of word by 1 
                    d[word] += 1
                else: 
                    # Add the word to dictionary with count 1 
                    d[word] = 1
        # Print the contents of dictionary 
        sort_orders = sorted(d.items(), key=lambda x: x[1], reverse=True) 
        for i in sort_orders:
            textFile.write(str(i[0]) + ":" + str(i[1]) + "\n" )