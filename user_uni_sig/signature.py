
import logging
import unicodedata
import user_uni_sig
from collections import Counter


class Signature():
    """_summary_

    Raises:
        TypeError: _description_
        TypeError: _description_
        ValueError: _description_
        ValueError: _description_

    Returns:
        _type_: _description_
    """

    __PUNCT_CAT = ['Pc','Pd','Pe','Pf','Pi','Po','Ps','Sc','Sk','Sm']

    def __init__(self, text_to_analyze:str,text_length_limit:int = 256):
        """Initilizes Signature object

        Args:
            text_to_analyze (str): Text that you want unicode signatures from
            text_length_limit (int, optional): Max length of text to analyze. Defaults to 256, no longer than 1024.

        Raises:
            TypeError: Throws a type error if anything other than a str is passed to be analyzed.
            TypeError: Throws a type error if a non-int is passed as the limit.
            ValueError: If a length limit longer than 1024 is passed, or a 0.
        """

        # input validation
        if not isinstance(text_to_analyze, str):
            raise TypeError('text_to_analyze must be a string')
        if not isinstance(text_length_limit, int):
            raise TypeError('text_length_limit must be an integer')
        
        if text_length_limit > 1024:
            raise ValueError('Only pass length limits less than 1024 characters')
        
        if text_length_limit == 0:
            raise ValueError('Only pass length limits less than 1024 characters')

        if int(len(text_to_analyze)) > text_length_limit:
            # slicing down to match length limit
            text_to_analyze = text_to_analyze[:text_length_limit]

        self.__text_original = text_to_analyze


    ### Private Functions ###

    def __convert_to_unicode_integers(self) -> list:
        """Converts the characters to unicode integer values.

        Returns:
            list: Contains the unicode integers representing the analysis text.
        """
                             
        unicode_integer_list = []

        for character in list(self.__text_original):
            uni_chart = ord(character)
            unicode_integer_list.append(uni_chart)

        return unicode_integer_list

    def __category_list(self) -> list:
        """Returns the pattern of unicode categories present in the string

        Returns:
            list: Pattern of unicode categories
        """

        signature_list = []

        for char in self.__text_original:
            cat = unicodedata.category(char)
            if not signature_list:
                # empty list
                signature_list.append(cat)
            elif signature_list[-1] == cat:
                # last item is the same
                pass
            else:
                # adding 
                signature_list.append(cat)

        return signature_list
    
    def __block_list(self) -> list:
        """Returns the pattern of unicode blocks present in the string.  Uses lows hex number in the block.

        Returns:
            list: Pattern of unicode blocks
        """

        signature_list = []

        for char in self.__text_original:
            cat = user_uni_sig.Block(char)
            if not signature_list:
                # empty list
                signature_list.append(cat.block_start)
            elif signature_list[-1] == cat.block_start:
                # last item is the same
                pass
            else:
                # adding 
                signature_list.append(cat.block_start)

        return signature_list
    
    def __block_label_list(self) -> list:
        """Returns the pattern of unicode block labels present in the string

        Returns:
            list: Pattern of unicode block labels
        """

        signature_list = []

        for char in self.__text_original:
            cat = user_uni_sig.Block(char)
            if not signature_list:
                # empty list
                signature_list.append(cat.label)
            elif signature_list[-1] == cat.label:
                # last item is the same
                pass
            else:
                # adding 
                signature_list.append(cat.label)

        return signature_list
    
    def __calculate_unicode_signature(self) -> list:
        """Returns the pattern of unicode blocks in the string, 
        but any character from a punctuation class is represented 
        by it's unicode category.

        Returns:
            list: Pattern of unicode blocks and punctuation in the string.
        """

        signature_list = []
        for char in self.__text_original:
            block_object = user_uni_sig.Block(char)
            category = unicodedata.category(char)

            next_sig = block_object.block_start

            if category in self.__PUNCT_CAT:
                next_sig = category

            if not signature_list:
                # empty list
                signature_list.append(next_sig)
            elif signature_list[-1] == next_sig:
                # last item is the same
                pass
            else:
                # adding 
                signature_list.append(next_sig)

        return signature_list
    
    def __calculate_unicode_signature_v2(self) -> list:
        """Returns of a pattern of unicode blocks in the string,
        but any character from a punctuation class is represented by
        it's class instead.  This version of the signature counts the
        number of characters by block or category, and denotes order.
        Data is represented as {order:{block/category:character count}}

        Returns:
            list: Pattern of unicode blocks & punctuation in the string
            with character counts.
        """

        signature_list = []

        text = self.__text_original
        
        block_list = []
        
        # convert to unicode blocks or categories
        for char in self.__text_original:
            
            block_object = user_uni_sig.Block(char)
            category = unicodedata.category(char)

            current_item = block_object.block_start
            
            if category in self.__PUNCT_CAT:
                current_item = category
                
            block_list.append(current_item)
        
        position = 0
        temp_counter = Counter()
        
        while block_list:
            
            # pop first character from list
            current_char = block_list.pop(0)
                
            if not block_list:
                # string is empty
                temp_counter[current_char] += 1
                temp_dict = {position: dict(temp_counter)}
                signature_list.append(temp_dict)
            elif current_char == block_list[0]:
                # increment
                temp_counter[current_char] += 1
            else:
                # mismatch and the list isn't empty
                temp_counter[current_char] += 1
                temp_dict = {position: dict(temp_counter)}
                signature_list.append(temp_dict)
                position += 1
                temp_counter.clear()

        return signature_list
    
    def __calculate_unicode_block_counts(self) -> dict:
        """_summary_

        Returns:
            dict: _description_
        """

        overall_counter = Counter()

        for char in self.__text_original:
            
            block_object = user_uni_sig.Block(char)
            category = unicodedata.category(char)

            current_item = block_object.block_start

            if category in self.__PUNCT_CAT:
                current_item = category

            if not overall_counter:
                # block not in counter yet
                overall_counter[current_item] += 1
            elif current_item in overall_counter.keys():
                # same item
                overall_counter[current_item] += 1
            else:
                # nothing to do
                continue

        return dict(overall_counter)
    
    def __calculate_punctuation_signature(self) -> list:
        """_summary_

        Returns:
            list: _description_
        """

        signature_list = []

        for char in self.__text_original:
            
            current_item = unicodedata.category(char)

            if current_item in self.__PUNCT_CAT:
                signature_list.append(current_item)

        return signature_list
    

    #####

    @property
    def text_original(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return self.__text_original
    
    @property
    def unicode_chars_integer_string(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        integer_list = self.__convert_to_unicode_integers()
        return "".join(str(integer_list))
    
    @property
    def unicode_chars_integer_list(self) -> list:
        """_summary_

        Returns:
            list: _description_
        """
        return self.__convert_to_unicode_integers()
    
    @property
    def unicode_category_signature(self) -> list:
        """Returns a signature consisting solely of the unicode blocks present

        Returns:
            list: Unicode block signature
        """
        return self.__category_list()
    
    @property
    def unicode_category_contains(self) -> set:
        """Returns a list of the unicode categories present in analyzed string

        Returns:
            set: Unique unicode categories present in the analyzed string
        """
        return set(self.unicode_category_signature)
    
    @property
    def unicode_block_signature(self) -> list:
        """Returns a signature consisting solely of the unicode blocks present

        Returns:
            list: Unicode block signature
        """
        return self.__block_list()
    
    @property
    def unicode_block_contains(self) -> set:
        """Returns a list of the unicode blocks present in analyzed string

        Returns:
            set: Unique unicode blocks present in the analyzed string
        """
        return set(self.__block_signature)
    
    @property
    def unicode_block_label_signature(self) -> list:
        """_summary_

        Returns:
            list: _description_
        """
        return self.__block_label_list()
    
    @property
    def unicode_signature(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.__calculate_unicode_signature()
    
    @property
    def unicode_signature_v2(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.__calculate_unicode_signature_v2()
    
    @property
    def unicode_block_counts(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.__calculate_unicode_block_counts()
    
    @property
    def punctuation_pattern(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.__calculate_punctuation_signature()