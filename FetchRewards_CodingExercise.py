#!/usr/bin/env python
# coding: utf-8

# In[1]:


sample1 = """The easiest way to earn points with Fetch Rewards is to just shop for the products you already love. If you have any participating brands on your receipt, you'll get points based on the cost of the products. You don't need to clip any coupons or scan individual barcodes. Just scan each grocery receipt after you shop and we'll find the savings for you."""
sample2 = """The easiest way to earn points with Fetch Rewards is to just shop for the items you already buy. If you have any eligible brands on your receipt, you will get points based on the total cost of the products. You do not need to cut out any coupons or scan individual UPCs. Just scan your receipt after you check out and we will find the savings for you."""
sample3 = """We are always looking for opportunities for you to earn more points, which is why we also give you a selection of Special Offers. These Special Offers are opportunities to earn bonus points on top of the regular points you earn every time you purchase a participating brand. No need to pre-select these offers, we'll give you the points whether or not you knew about the offer. We just think it is easier that way."""

sample1 = sample1.lower()
sample2 = sample2.lower()
sample3 = sample3.lower()


# In[2]:


def clean_data(s):
    punctuations = ".,:;\\!?\""
    contractions = {"n't" : " not", "'ve" : " have", "'ll" : " will"}
    for i in punctuations:
        s = s.replace(i, "")
    
    for j in contractions.keys():
        s = s.replace(j, contractions[j])
    
    return s

def words_to_dict(s):
    wd = {}
    list_s = s.split(" ")
    for i in list_s:
        if(len(i)>2):
            if(i in wd.keys()):
                wd[i] += 1
            else:
                wd[i] = 1
    return wd

def doing_dats(vocab, w):
    temp_list = []
    for i1 in range(len(vocab.items())):
            temp_list.append(0)

    for item in vocab.keys():
        if(item in w.keys()):
            temp_list[vocab[item]] = 1
    return temp_list

def process_sample(sample1, sample2):
    w1 = words_to_dict(clean_data(sample1))
    w2 = words_to_dict(clean_data(sample2))
    all_words = list(w1.keys())
    all_words.extend(list(w2.keys()))
    all_words = list(set(all_words))
    all_words.sort()
    #n = len(all_words)
    #return (similarity_check1(w1,w2,n))
    return (w1,w2,all_words)

# Jaccard Similarity
def similarity_check1(dict1, dict2, n):
    common1 = len(list(set(dict1) & set(dict2)))
    similarity1 = common1/n
    return(round(similarity1,5))

# Cosine Similarity
def similarity_check2(main_list, w1, w2):
    numer = 0
    for p2 in range(len(main_list[0])):
        numer += main_list[0][p2] * main_list[1][p2]

    den1 = 0
    for p3 in range(len(main_list[0])):
        den1 += main_list[0][p3] ** 2 #main_list[0][p3]
    den2 = 0
    for p4 in range(len(main_list[1])):
        den2 += main_list[1][p4] ** 2 #main_list[1][p4]
        
    denr = (den1*den2) ** (1/2)
    return(round((numer/denr),5))


# In[15]:


s = [sample1, sample2, sample3]


# In[ ]:


def exec_similarity1(s):
    results = []
    for i in range(len(s)-1):
        for j in range(i+1,len(s)):
            (d1, d2, all_words) = process_sample(s[i], s[j])
            n = len(all_words)
            result = similarity_check1(d1, d2, n)
            print("Similarity Measure 1 between Sample "+str(i+1)+" and "+str(j+1)+"     ---> "+str(result))
            results.append(result)
    return results


# In[16]:


def exec_similarity2(s):
    results = []
    for i in range(len(s)-1):
        for j in range(i+1,len(s)):
            (d1, d2, all_words) = process_sample(s[i], s[j])

            vocab = {}
            for ind, word in enumerate(all_words):
                vocab[word] = ind
            main_list = []
            list1 = doing_dats(vocab, d1)
            list2 = doing_dats(vocab, d2)
            main_list.append(list1)
            main_list.append(list2)
            result = similarity_check2(main_list, d1, d2)
            print("Similarity Measure 2 between Sample "+str(i+1)+" and "+str(j+1)+"     ---> "+str(result))
            results.append(result)
    return results


# In[21]:


r1 = exec_similarity1(s)
print("-------------------------------------------------------------")
r2 = exec_similarity2(s)
print("-------------------------------------------------------------")
for i in range(len(r1)-1):
    for j in range(i+1,len(r1)):
        print("Final Similarity Measure between Sample "+str(i+1)+" and "+str(j+1)+" ---> "+str((r1[i]+r2[i])/2))


# In[6]:


# BELOW CODE DID NOT HAVE GOOD OUTPUTS ON OUR CURRENT SAMPLE - NOT PART OF SOLUTION


# # TF-IDF
"""
s1 = clean_data(sample1); s2 = clean_data(sample2); s3 = clean_data(sample3);

s1_list = s1.split(" ")
s2_list = s2.split(" ")
s3_list = s2.split(" ")
df1 = {}; df2 = {}; df3 = {};

# FUNCTIONS START
def doc_len(doc_list):
    temp = [x for x in doc_list if len(x)>2]
    return(len(temp))

def words_to_dict(list_s):
    wd = {}
    #list_s = s.split(" ")
    for i in list_s:
        if(len(i)>2):
            if(i in wd.keys()):
                wd[i] += 1
            else:
                wd[i] = 1
    return wd

def tf_calc(vocab, df, doc_len):
    temp_list = []
    for i in range(len(vocab.items())):
        temp_list.append(0)
    for item in vocab.keys():
        if(item in df.keys()):
            temp_list[vocab[item]] = df[item]/doc_len
    return temp_list

def ln(x):
    n = 1000.0
    return n * ((x ** (1/n)) - 1)

def tfidf(idf, main_list2, vocab1, n):
    temp_list = []
    for i1 in range(len(vocab1.items())):
        temp_list.append(0)
    for i in range(len(temp_list3)):
        temp_list[i] = idf[i] * main_list2[n][i]
    return temp_list

# FUNCTIONS END

# Getting document length
doc1_len = doc_len(s1_list)
doc2_len = doc_len(s2_list)
doc3_len = doc_len(s3_list)

# Converting sentences to a dictionary bag of words
df1 = words_to_dict(s1_list)
df2 = words_to_dict(s2_list)
df3 = words_to_dict(s3_list)

# Creating a vocab of all the documents/samples
all_words_list = list(set(df1.keys()).union(set(df2.keys())).union(set(df2.keys())))
all_words_list.sort()
vocab1 = {}
vocab2 = {}
for i in range(len(all_words_list)):
    vocab1[all_words_list[i]] = i
    vocab2[all_words_list[i]] = 0

# Calculating the Term Frequencies
main_list2.append(tf_calc(vocab1, df1, doc_len1))
main_list2.append(tf_calc(vocab1, df2, doc_len2))
main_list2.append(tf_calc(vocab1, df3, doc_len3))

# Getting the number of sentences containing the word
for i in vocab2.keys():
    if i in df1.keys():
        vocab2[i] += 1
    if i in df2.keys():
        vocab2[i] += 1
    if i in df3.keys():
        vocab2[i] += 1
        
# IDF Calc
for j in vocab2.keys():
    vocab2[j] = ln(3/vocab2[j])
idf = list(vocab2.values())

# Getting the TF-IDF Values
tfidf = []
tfidf.append(tfidf(idf, main_list2, vocab1, 0))
tfidf.append(tfidf(idf, main_list2, vocab1, 1))
tfidf.append(tfidf(idf, main_list2, vocab1, 2))
#print(tfidf)

# Doing cosine similarity for sample1 and sample2
numer = 0
for i in range(len(tfidf[0])):
    numer += tfidf[0][i]*tfidf[1][i]

den1 = 0
for j in range(len(main_list[0])):
    den1 += main_list[0][j] ** 2

den2 = 0
for k in range(len(main_list[1])):
    den2 += main_list[1][k] ** 2
    
"""
# In[ ]:


# ABOVE TF-IDF CODE DID NOT HAVE GOOD OUTPUTS ON OUR CURRENT SAMPLE - NOT PART OF SOLUTION

