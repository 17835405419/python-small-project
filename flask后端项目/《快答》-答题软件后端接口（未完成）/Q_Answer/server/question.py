"""
作者：zwq
日期:2022年08月17日
"""
from model import Question


def add(question_info):
    question = Question(subject=question_info["subject"], answer=question_info["answer"].split('|'),
                        answerTrue=question_info["answerTrue"].split('|'), analysis=question_info["analysis"],
                        classification=question_info["classification"])
    question.save()


# 查询相关

def find_one(questionId):
    """ 根据Id获取问题 """
    question_info = Question.objects(questionId=questionId).first()
    return question_info

def findAll_class(classification,limitNum=0):
    """ 根据分类查询问题 """
    question_list = Question.objects(classification=classification).limit(limitNum)
    return question_list
