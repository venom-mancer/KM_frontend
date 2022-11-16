from collections import Counter, defaultdict 
import re


# p = re.compile(r'{}'.format())


def clean_text(text):
    """
    takes the text and removes signs and some extra words
    """
    stopwords = {
        'از','به','با','در','بر','برای','بی','درباره',
        'تا','را','بدون','چون','مانند','مثل','زیر','روی','است','هست','شد',
        'مگر','الا','.','،','؛',':','؟','!','[',']','(',')'
    }
    result  = [word for word in re.split("\W+",text) if word.lower() not in stopwords]
    result = (' ').join(result)
    return result



def match_text_pattern_dictionary(pattern,text):
    """
    takes the pattern and a text and returns a dictionary of words with the list of their starting indexes and endings
    """
    d = defaultdict(list)
    for m in pattern.finditer(text):
        word_index_begin = m.start()
        word_index_end = m.end()
        word = m.group()
        d[word].append((word_index_begin,word_index_end))

    return d


def spaces_between_words_dict(pattern,text):
    """
    takes the pattern and text then returns the dict of words with spaces between them 

    """

    # makes the text clean
    text = clean_text(text)

    dict = match_text_pattern_dictionary(pattern=pattern , text= text)

    d = {}
    counter_list = []
    list_this_word_spaces = []

    counter = Counter(re.split('[\s|,]', text))
    for key in dict:
        counter_list.append(counter['{}'.format(key)])

    for word  in dict:
        this_word_values = dict[word]

        count = 0
        if len(this_word_values) > 1:
            
            for i in this_word_values:
                start_slice = i[1]
                end_slice_tuple = this_word_values[count+1]
                end_slice = end_slice_tuple[0]
                count += 1
                len_text_between_two_match = len(text[start_slice:end_slice].split())
                list_this_word_spaces.append(len_text_between_two_match)
                
                if count+1 == len(this_word_values):
                    break
        
        else:
            d[word] = 0

    values_lower_than_distance = sum(i < 6 for i in list_this_word_spaces)

    point = sum(counter_list) + (values_lower_than_distance * 7)
    return point




# space_words_dict = spaces_between_words_dict(pattern=p , text= long_string)

# print('hellow ')

