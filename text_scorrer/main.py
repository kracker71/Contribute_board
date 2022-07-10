from text_scorrer import TextScorrer
# from utils import splitter

def main():
    scorrer = TextScorrer()
    sentence1 = "เห้อออออ... เจอ river แบบนี้ โคตรเซ็ง อยากเอาหัวโขกกำแพง คงต้องลองเล่นดู"
    print(scorrer.get_score_and_class(sentence1))

if __name__ == "__main__":
    main()