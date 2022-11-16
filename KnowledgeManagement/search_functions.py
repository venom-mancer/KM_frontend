"""
search functions for knowledge

"""


def knowledge_advance_search(knowledges ,from_date=0 , to_date=0,search_title = 0,search_keyword = 0,creator_user = 0 ):
    if from_date != 0 or to_date !=0:
        if from_date and to_date:
            from_date = int(''.join(from_date.split('/')))
            to_date = int(''.join(to_date.split('/')))
            knowledges = knowledges.filter(
                KnowledgeFromDate__gte=from_date,
                KnowledgetoDate__lte=to_date)

        elif to_date == "" and not from_date == "":
            from_date = int(''.join(from_date.split('/')))
            knowledges = knowledges.filter(KnowledgeFromDate__gte=from_date)

        elif from_date == "" and not to_date == "":
            to_date = int(''.join(to_date.split('/')))
            knowledges = knowledges.filter(KnowledgetoDate__lte=to_date)


    if search_title != 0:
        if search_title is not None and search_title != "":
            knowledges = knowledges.filter(KnowledgeTitle__contains =search_title)

    if search_keyword != 0:
        if len(search_keyword) != 0 and search_keyword is not None:
            search_keyword = search_keyword[0].split(' ')
            del search_keyword[-1]
            search_keyword = '|'.join(search_keyword)
            search_keyword = search_keyword

            knowledges = knowledges.filter(KnowledgeKeywords__regex=r'({})'.format(search_keyword))


    if creator_user != 0:
        if creator_user is not None and int(creator_user) != -1:
            knowledges = knowledges.filter(CreatorUserID=creator_user)

    return knowledges