
def test_short_phrase():
    assert 15 > len(str(input("Set a phrase: ")).strip()), "Phrase has more than 15 characters"