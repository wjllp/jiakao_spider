from dao import mydao
if __name__ == '__main__':
    email = input('请输入邮箱：')
    kskm = input('请输入考试科目（科目一即输入数字1）：')
    kcmc = input('请输入考场名称（全名）：')
    mydao.insert_user(email,kcmc,int(kskm))
