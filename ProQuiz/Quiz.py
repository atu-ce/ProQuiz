# Question
class Question:
    def __init__(self, text, answer):
        self.text    = text
        self.answer  = answer

    # Kullanıcının verdiği cevabın doğruluğunu ölçer.
    def checkAnswer(self, answer):
        return self.answer == answer

    def getAnswer(self):
        return self.answer

# Quiz
class Quiz:
    trueAnswers = []
    falseAnswers = []

    def __init__(self, questions):
        self.questions = questions
        self.score = 0
        self.questionIndex = 0

    # Bu fonksiyonun amacı, o anki 'questionIndex'in değerine karşılık gelen  question objesini göndermek.
    def getQuestion(self):
        return self.questions[self.questionIndex]

    # Bu fonksiyon, gelen question objesini ekrana yazdırır.
    def disPlayQuestion(self):
        question = self.getQuestion()
        print(f"Soru {self.questionIndex + 1}: {question.text}")

        answer = input("Cevap: ").lower().strip()
        self.guess(answer) # guess -> tahmin
        self.loadQuestion()

    # Bu fonksiyonun amacı, koşulsuz index numarasını arttırmak ve
    # 'checkAnswer'dan gelen değer 'True' ise score değiskenini arttırmak.
    def guess(self, answer):
        question = self.getQuestion()

        if question.checkAnswer(answer):
            self.score += 1
            self.isTrue(answer)
        else:
            self.isFalse(answer)

        self.questionIndex += 1

    # İndex aşımını kontrol eder.
    def loadQuestion(self):
        if len(self.questions) == self.questionIndex:
            self.showScore()
        else:
            self.disPlayProgress()
            self.disPlayQuestion()

    # Quizi bitirir ve kullanıcıya skorunu gösterir.
    def showScore(self):
        print(" Results ".center(100, '*'))
        print(f"Quiz bitti. Score: {self.score}")

        print("\nDoğru cevaplarınız:")
        for i in self.trueAnswers:
            print(i)

        print("\nYanlış cevaplarınız:")
        for i in self.falseAnswers:
            print(i)

        print(" Finish ".center(100,'*'))

    # Kullanıcıya kaç sorudan kaçıncıda olduğunu gösterir.
    def disPlayProgress(self):
        totalQuestion = len(self.questions)
        questionNumber = self.questionIndex + 1

        print(f" Question {questionNumber} of {totalQuestion} ".center(100, '*'))
    
    # Kullanıcıya hangi soruya doğru, hangisine yanlış cevap verdiğini göstermeliyiz;
    # ** Doğru ise bu fonksiyon çalışır.
    def isTrue(self, answer):
        question = self.getQuestion()
        self.trueAnswers.append(f"{self.questionIndex + 1}. soru ({answer}).")

    # ** Yanlış ise bu fonksiyon çalışır.
    def isFalse(self, answer):
        question = self.getQuestion()
        getAnswer = question.getAnswer()
        self.falseAnswers.append(f"{self.questionIndex + 1}. soru ({answer}), doğru cevap: {getAnswer}.")

# 1'e basıldığında bu fonksiyon çalışır. Yeni soru ekler.
def questionAppend():
    soru = input("Soru: ").strip()
    cevap = input("Cevap: ").lower().strip()

    with open("QuestionsAndAnswers.txt", "a", encoding = "utf-8") as dosya:
        dosya.write(f"{soru}: {cevap}\n")

# 2'ye basıldığında bu fonksiyon çalışır. Quizi başlatır.
def quizStart():
    questions = []
    with open("QuestionsAndAnswers.txt", "r", encoding = "utf-8") as dosya:
        for satir in dosya:
            satir = satir[ : -1]
            liste = satir.split(":")

            questions.append(Question(liste[0], liste[1].lower().strip()))

    quiz = Quiz(questions)
    quiz.loadQuestion()

# Menünün oluşturulduğu bölüm
while True:
    islem = input("1.) Soru ekle\n2.) Sınava başla\n3.) Çıkış\n")

    if islem   == "1":
        questionAppend()

    elif islem == "2":
        quizStart()

    elif islem == "3":
        break

    else:
        print("Yanlış değer girdiniz. Lütfen tekrar deneyiniz.")

"""
    Ufak bir mantık hatası, gözden kaçan, önemsiz gibi gözüküp, kod dizininin iskeletini oluşturan şey sizi tüm gün uğraştırabilir... :)
"""


