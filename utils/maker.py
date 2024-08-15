from faker import Faker

faker = Faker()

def make_sentence(sentence_length):
    return faker.sentence(nb_words=sentence_length)