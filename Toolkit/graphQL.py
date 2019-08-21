#!/usr/bin/env python
# -*- coding:utf-8 -*-

from graphene.types.resolver import dict_resolver
import graphene
import sys
import os
import json
import re

from pprint import pprint

# Articut Result 檔案路徑
resultFilePath = ''


"""
Articut GraphQL Schema
"""
class Persons(graphene.ObjectType):
    class Meta:
        default_resolver = dict_resolver
    
    text = graphene.String()
    pos_ = graphene.String()
    tag_ = graphene.String()

class Nouns(graphene.ObjectType):
    class Meta:
        default_resolver = dict_resolver
    
    text = graphene.String()
    pos_ = graphene.String()
    tag_ = graphene.String()

class Numbers(graphene.ObjectType):
    class Meta:
        default_resolver = dict_resolver
    
    text = graphene.String()
    pos_ = graphene.String()
    tag_ = graphene.String()

class Sites(graphene.ObjectType):
    class Meta:
        default_resolver = dict_resolver
    
    text = graphene.String()
    pos_ = graphene.String()
    tag_ = graphene.String()

class Userdefined(graphene.ObjectType):
    class Meta:
        default_resolver = dict_resolver
    
    text = graphene.String()
    pos_ = graphene.String()
    tag_ = graphene.String()

class Meta(graphene.ObjectType):
    class Meta:
        default_resolver = dict_resolver
    
    lang = graphene.String()
    description = graphene.String()

class Tokens(graphene.ObjectType):
    class Meta:
        default_resolver = dict_resolver
    
    text = graphene.String()
    pos_ = graphene.String()
    tag_ = graphene.String()
    isStop = graphene.Boolean()
    isEntity = graphene.Boolean()
    isVerb = graphene.Boolean()
    isTime = graphene.Boolean()
    isClause = graphene.Boolean()
    isKnowledge = graphene.Boolean()

class Ents(graphene.ObjectType):
    class Meta:
        default_resolver = dict_resolver
    
    persons = graphene.List(Persons)
    nouns = graphene.List(Nouns)
    numbers = graphene.List(Numbers)
    sites = graphene.List(Sites)
    #userdefined = graphene.List(Userdefined)

class Doc(graphene.ObjectType):
    class Meta:
        default_resolver = dict_resolver
    
    text = graphene.String()
    tokens = graphene.List(Tokens)
    ents = graphene.Field(Ents)

class Nlp(graphene.ObjectType):
    meta = graphene.Field(Meta)
    doc = graphene.Field(Doc)

class Query(graphene.ObjectType):
    nlp = graphene.Field(
        Nlp,
        filepath = graphene.String(),
        model = graphene.String()
    )
    
    def resolve_nlp(self, info, filepath, model):
        if model != "TW":
            return Nlp(
                meta = {
                    "lang": model,
                    "description": 'Articut-GraphQL Model Unsupported.'
                }
            )
        
        if filepath[-5:] == '.json':
            try:
                with open(filepath, 'r', encoding='utf-8') as resultFile:
                    result = json.loads(resultFile.read())
                textTagLIST = posList2TextTag(result["result_pos"])
                
                return Nlp(
                    meta = {
                        "lang": model,
                        "description": 'Articut GraphQL Query Result.'
                    },
                    doc = {
                        "text": result["result_segmentation"].replace('/', ''),
                        "tokens": getTokens(textTagLIST),
                        "ents": getEnts(textTagLIST)
                    }
                )
            except Exception as e:
                print('[Articut-GraphQL ERROR] {}'.format(e))
        return Nlp(
            meta = {
                "lang": model,
                "description": 'Articut-GraphQL Error.'
            }
        )


"""
Used by ArticutAPI.py
"""
class GraphQL():
    def query(self, filePath, query="""
    {
      meta {
        lang
        description
      }
      doc {
        text
        tokens {
          text
          pos_
          tag_
          isStop
          isEntity
          isVerb
          isTime
          isClause
          isKnowledge
        }
        ents {
          persons {
            text
            pos_
            tag_
          }
          nouns {
            text
            pos_
            tag_
          }
          numbers {
            text
            pos_
            tag_
          }
          sites {
            text
            pos_
            tag_
          }
        }
      }
    }"""):
        query = """{\n  nlp(filepath: "{{filePath}}", model: "TW") {{query}}\n}""".replace('{{filePath}}', filePath).replace('{{query}}', query)
        result = graphene.Schema(query=Query).execute(query)
        return json.loads(json.dumps({"data": result.data}))

"""
將 result_pos 拆開成 [{"text", "tag_", "pos_"} ...]
"""
def posList2TextTag(posLIST):
    textTagLIST = []
    textPosPat = re.compile("<[^>]*?>.*?</[^>]*?>")
    posPat = re.compile("(?<=>).*?</[^>]*?>")
    posLIST.reverse()
    for pos in posLIST:
        if pos[0] == '<' and pos[-1] == '>':
            textPosLIST = [p.group(0) for p in reversed(list(textPosPat.finditer(pos)))]
            for t in textPosLIST:
                textLIST = [tp.group(0).split("</") for tp in posPat.finditer(t)]
                textTagLIST.append({
                    "text": textLIST[0][0],
                    "tag_": textLIST[0][1][:-1],
                    "pos_": pos2UniversalPOS(textLIST[0][1][:-1])
                })
        else:
            textTagLIST.append({
                "text": pos,
                "tag_": 'PUNCTUATION',
                "pos_": 'PUNCT'
            })
    textTagLIST.reverse()
    return textTagLIST

"""
Articut POS 轉換 Universal Part-of-speech Tags
"""
def pos2UniversalPOS(pos):
    if pos in ['FUNC_inner']:
        return 'ADP'
    if pos in ['FUNC_determiner']:
        return 'DET'
    if pos in ['AUX', 'MODAL']:
        return 'AUX'
    if pos in ['ASPECT', 'FUNC_negation']:
        return 'PART'
    if pos in ['FUNC_inter', 'FUNC_conjunction']:
        return 'CONJ'
    if pos in ['ENTITY_person', 'ENTITY_pronoun']:
        return 'PERSON'
    if pos in ['TIME_justtime', 'RANGE_period']:
        return 'TIME'
    if pos in ['QUANTIFIER', 'ENTITY_measurement']:
        return 'QUANTITY'
    if pos in ['MODIFIER', 'MODIFIER_color', 'FUNC_modifierHead']:
        return 'ADJ'
    if pos in ['LOCATION', 'RANGE_locality', 'KNOWLEDGE_place', 'KNOWLEDGE_addTW', 'KNOWLEDGE_route']:
        return 'LOC'
    if pos in ['VerbP', 'ACTION_verb', 'ACTION_lightVerb', 'ACTION_quantifiedVerb']:
        return 'VERB'
    if pos in ['TIME_day', 'TIME_week', 'TIME_month', 'TIME_season', 'TIME_year', 'TIME_decade', 'TIME_holiday']:
        return 'DATE'
    if pos in ['IDIOM', 'ENTITY_noun', 'ENTITY_nouny', 'ENTITY_oov', 'ENTITY_NP', 'ENTITY_nounHead', 'ENTITY_num', 'ENTITY_classifier', 'ENTITY_possessive']:
        return 'NOUN'

    return 'OTHER' # ['UserDefined', 'CLAUSE_AnotAQ', 'CLAUSE_YesNoQ', 'CLAUSE_WhoQ', 'CLAUSE_WhatQ', 'CLAUSE_WhereQ', 'CLAUSE_WhenQ', 'CLAUSE_HowQ', 'CLAUSE_WhyQ', 'CLAUSE_Particle', 'KNOWLEDGE_url']

"""
Articut-GraphQL Content
"""
def getTokens(textTagLIST):
    resultLIST = []
    for textTag in textTagLIST:
        resultDICT = {
            "text": textTag["text"],
            "tag_": textTag["tag_"],
            "pos_": textTag["pos_"],
            "isStop": posIsStop(textTag["tag_"]),
            "isEntity": posIsEntity(textTag["tag_"]),
            "isVerb": posIsVerb(textTag["tag_"]),
            "isTime": posIsTime(textTag["tag_"]),
            "isClause": posIsClause(textTag["tag_"]),
            "isKnowledge": posIsKnowledge(textTag["tag_"])
        }
        resultLIST.append(resultDICT)
    return resultLIST

def getEnts(textTagLIST):
    resultDICT = {
        "persons": getPersons(textTagLIST),
        "nouns": getNouns(textTagLIST),
        "numbers": getNumbers(textTagLIST),
        "sites": getSites(textTagLIST)
        #"userdefined": getUserdefined(textTagLIST)
    }
    return resultDICT

"""
Articut-GraphQL Function
"""
def posIsStop(pos):
    if pos in ['ACTION_lightVerb', 'FUNC_determiner', 'FUNC_modifierHead', 'FUNC_negation', 'FUNC_conjunction', 'RANGE_locality', 'RANGE_period']:
        return True
    return False

def posIsEntity(pos):
    if pos in ['ENTITY_num', 'ENTITY_classifier', 'ENTITY_measurement', 'ENTITY_person', 'ENTITY_pronoun', 'ENTITY_possessive', 'ENTITY_noun', 'ENTITY_nounHead', 'ENTITY_nouny', 'ENTITY_oov', 'ENTITY_NP']:
        return True
    return False

def posIsVerb(pos):
    if pos in ['ACTION_verb', 'ACTION_quantifiedVerb', 'VerbP']:
        return True
    return False

def posIsTime(pos):
    if pos in ['TIME_justtime', 'TIME_holiday', 'TIME_day', 'TIME_week', 'TIME_month', 'TIME_season', 'TIME_year', 'TIME_decade']:
        return True
    return False

def posIsClause(pos):
    if pos in ['CLAUSE_AnotAQ', 'CLAUSE_YesNoQ', 'CLAUSE_WhoQ', 'CLAUSE_WhatQ', 'CLAUSE_WhereQ', 'CLAUSE_WhenQ', 'CLAUSE_HowQ', 'CLAUSE_WhyQ', 'CLAUSE_Particle']:
        return True
    return False

def posIsKnowledge(pos):
    if pos in ['KNOWLEDGE_addTW', 'KNOWLEDGE_url', 'KNOWLEDGE_place', 'KNOWLEDGE_route', 'LOCATION', 'UserDefined']:
        return True
    return False

def getPersons(textTagLIST):
    resultLIST = []
    for textTag in textTagLIST:
        if textTag["tag_"] in ['ENTITY_person', 'ENTITY_pronoun']:
            resultLIST.append(textTag)
    return resultLIST

def getNouns(textTagLIST):
    resultLIST = []
    for textTag in textTagLIST:
        if textTag["tag_"] in ['ENTITY_noun', 'ENTITY_nounHead', 'ENTITY_nouny', 'ENTITY_oov', 'ENTITY_NP']:
            resultLIST.append(textTag)
    return resultLIST

def getNumbers(textTagLIST):
    resultLIST = []
    for textTag in textTagLIST:
        if textTag["tag_"] in ['ENTITY_num', 'ENTITY_classifier', 'ENTITY_measurement']:
            resultLIST.append(textTag)
    return resultLIST

def getSites(textTagLIST):
    resultLIST = []
    for textTag in textTagLIST:
        if textTag["tag_"] in ['KNOWLEDGE_addTW', 'KNOWLEDGE_place', 'LOCATION', 'KNOWLEDGE_route']:
            resultLIST.append(textTag)
    return resultLIST

# Uncompleted
def getUserdefined(textTagLIST):
    resultLIST = []
    for textTag in textTagLIST:
        if textTag["tag_"] in ['']:
            resultLIST.append(textTag)
    return resultLIST



"""
Used by python ArticutGraphQL.py articutResult.json
Starlette server (http://0.0.0.0:8000)
"""
def serverStart():
    from starlette.applications import Starlette
    from starlette.routing import Router
    from starlette.routing import Route
    import uvicorn
    
    app = Router([Route('/', endpoint=graphQL, methods=['GET', 'POST'])])
    uvicorn.run(app, host='0.0.0.0', port=8000)
    return None

async def graphQL(request):
    from starlette.templating import Jinja2Templates
    from starlette.status import HTTP_400_BAD_REQUEST
    from starlette.responses import PlainTextResponse
    from starlette.responses import JSONResponse
    
    if request.method == 'POST':
        content_type = request.headers.get("Content-Type", "")
        if content_type == 'application/json':
            data = await request.json()
        else:
            return PlainTextResponse('Bad Request!', status_code=HTTP_400_BAD_REQUEST)
        
        try:
            query = data["query"]
            variables = data.get("variables")
        except KeyError:
            return PlainTextResponse('Bad Request!', status_code=HTTP_400_BAD_REQUEST)
        
        result = graphene.Schema(query=Query).execute(query, variables=variables)
        return JSONResponse({"data": result.data})
    else:
        return Jinja2Templates(directory='Toolkit').TemplateResponse('graphQL.html', {
            "request": request,
            "resultFilePath": resultFilePath
        })

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        resultFilePath = sys.argv[1]
        if os.path.isfile(resultFilePath):
            serverStart()
        else:
            print('{} 檔案不存在！'.format(resultFilePath))
    else:
        print('請輸入斷詞結果檔案路徑，例：python ArticutGraphQL.py articutResult.json')