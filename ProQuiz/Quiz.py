import datetime
import os

isStarted = False

def registrationFailed():
    global isStarted
    isStarted = False

def userCreated():
    global isStarted
    isStarted = True

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
    name = []
    surname = []

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
            self.create()
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

    # Kullanıcıdan isim-soyisim istenir ve gelen değer ile klasör oluşturulur.
    def kayitOl(self):
        isim = input("İsim: ").lower().strip()
        soyisim = input("Soyisim: ").lower().strip()

        way = os.path.dirname(os.path.abspath(__file__))
        path = f"{way}/users/{isim}_{soyisim}"

        try:
            os.mkdir(path)
        except OSError as err:
            print (f"{isim}_{soyisim} kullanıcısı {err} nedeninden dolayı oluşturulamadı")
            registrationFailed()
        else:
            print (f"{isim}_{soyisim} kullanıcısı başarıyla oluşturuldu")

            with open("loginInquiry.txt", "a", encoding = "utf-8") as dosya:
                dosya.write(f"{isim}_{soyisim}\n")

            userCreated()

        self.name.append(isim)
        self.surname.append(soyisim)

    def girisYap(self):
        global isStarted
        isim = input("İsim: ").lower().strip()
        soyisim = input("Soyisim: ").lower().strip()

        while True:
            try:
                with open("loginInquiry.txt", "r", encoding = "utf-8") as dosya:
                    for i in dosya:
                        user = i[: -1]
                        if f"{isim}_{soyisim}" == user:
                            isStarted = True
                            break
                    else:
                        print(f"Girmiş olduğunuz {isim}_{soyisim} adında kullanıcı sistemde kayıtlı değildir.")
            except:
                with open("loginInquiry.txt", "x", encoding = "utf-8") as dosya:
                    pass
            else:
                break

        self.name.append(isim)
        self.surname.append(soyisim)

    # Sınav bitiminde bu fonksiyon çalışır, giriş yapan kullanıcının klasörüne o anki 'tarih-saat.txt' dosyası oluşturulur ve doğru-yanlış cevap tablosu dosyaya eklenir.
    def create(self):
        now = datetime.datetime.now()
        tarih = datetime.datetime.strftime(now, '%d_%m_%Y') # Gün_Ay_Yıl
        saat = str(now.hour) + "_" + str(now.minute) + "_" + str(now.second)

        with open(f"users\{self.name[0]}_{self.surname[0]}\{tarih}_{saat}.txt", "a", encoding = "utf-8") as dosya:
            dosya.write("Doğru cevaplarınız:\n")

            for i in self.trueAnswers:
                dosya.write(f"{i}\n")

            dosya.write("\nYanlış cevaplarınız:\n")
            for i in self.falseAnswers:
                dosya.write(f"{i}\n")

            dosya.write("\n")

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
        # Soru eklemeyi sadece admin and editor yapabilmesi için gerekli kod dizini.
        access = input("Username(admin/editor): ").lower().strip()
        password = input("password(112233): ").strip()
        if ((access == "admin") or (access == "editor")) and (password == "112233"):
            questionAppend()
        else:
            print("Yanlış değer girdiniz.")

    elif islem == "2":
        while True:
            user = input("1.) Kayıt ol\n2.) Giriş yap\n")

            if user == "1":
                Quiz(True).kayitOl()
                break
            elif user == "2":
                Quiz(True).girisYap()
                break
            else:
                print("Yanlış değer girdiniz. Lütfen tekrar deneyiniz.")

        if isStarted:
            quizStart()
        break

    elif islem == "3":
        break

    else:
        print("Yanlış değer girdiniz. Lütfen tekrar deneyiniz.")

"""
    Ufak bir mantık hatası, gözden kaçan, önemsiz gibi gözüküp, kod dizininin iskeletini oluşturan şey sizi tüm gün uğraştırabilir... :)
"""


