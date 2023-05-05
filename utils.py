def grab_sculptor(s: str, prefix='Category:Sculptures by') -> str:
    remainder = s.split(prefix)
    if len(remainder) == 2:
        return remainder[1]
    elif len(remainder) == 1:
        assert remainder[0] == s
        return grab_sculptor(s, 'Category:')
    else:
        raise NotImplementedError('Check & Guess, PR welcome')
