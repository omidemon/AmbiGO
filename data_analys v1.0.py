import nltk, re

"""
    AmbiGO, the automated ambiguity detection tool
    Copyright (C) 2017,  Reza Khezri

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation version 3.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details:
    <http://www.gnu.org/licenses/>
"""

""" Google search API module"""
import json, requests
key = [please obtain yours]
cx = [please obtain yours]
url = "https://www.googleapis.com/customsearch/v1"

def query_hit(q):
    parameters = {"q": q, "exactTerms" : q, "cx": cx, "key": key, "googlehost" : "www.google.com"}
    page = requests.request("GET", url, params=parameters, verify=False)
    results = json.loads(page.text)
    if "error" in results:
        print results["error"].values()
    else:
        return results["searchInformation"]["totalResults"]


def googla(q1, q2):
    hits = {}
    (a, b) = (int(query_hit(q1)), int(query_hit(q2)))
    hits[q1] = a
    hits[q2] = b
    return hits

        
def ambRatioEval(hits):
    (minHit, maxHit) = sorted(hits, key=hits.__getitem__)
    total = sum(hits.values())
    if total > 0:
        if hits[maxHit] != 0:
            ambRatio = float(hits[minHit]) / float(hits[maxHit])
            return (ambRatio, hits)
        else: return None
    else: return None


def bestReadingFinder(R1, R2, maxHit):
    if maxHit in R1:
        return R1
    else:
        return R2

""" END """


sent_tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')


linkingV = ["am", "is", "are",
            "was", "were", "being", "been",
            "seem", "seems", "seemed",
            "sound", "sounded", "sounds",
            "become", "became", "becomes",
            "remain", "remains", "remained",
            "feel", "feels",  "felt",
            "appear", "appears", "appeared",
            "look", "looks", "looked"]

def RE_pars(toks, amb_patt):
    tagged = nltk.pos_tag(toks)
    cp = nltk.RegexpParser(amb_patt)
    parsed_tag = cp.parse(tagged)
    fishNet = []
    for item in parsed_tag:
        for chunk in item:
            if type(chunk)==tuple:
                fishNet.append(chunk)
    return fishNet


def syntactic(sent):
    stag = "<a href=''><span style='background:%s; color:white' title='syntactic ambiguity, type %s. %s'>"
    etag = "</span></a>"
    toks = nltk.word_tokenize(sent)
    tagged = nltk.pos_tag(toks)
    Anal_patt = "analytical: {<JJ><NN.*><NN.*>}"
    Coor_patt = "coordination: {<JJ><NN.*><CC><NN.*>}"
    PPA_patt = "PPAttachment: {<VB.*><DT>?<JJ>*<NN.*><IN><DT>?<JJ>*<NN.*>}"
    anal_fishNet = RE_pars(toks, Anal_patt)
    coor_fishNet = RE_pars(toks, Coor_patt)
    PPA_fishNet = RE_pars(toks, PPA_patt)
    amb_case = []

    ##English grammar teacher / modern economy teacher"""
    if anal_fishNet!=[]:
        for (w, t) in anal_fishNet:
            amb_case.append(w)

        q1 = "%s %s" % (amb_case[0], amb_case[1])
        q2 = "%s %s" % (amb_case[0], amb_case[2])
        reading1 = amb_case[2] + " of " + amb_case[0] + " " + amb_case[1]
        reading2 = amb_case[0] + " " + amb_case[2] + " of " + amb_case[1]
        hits = googla(q1, q2)
        ambRatio = ambRatioEval(hits)
        print ambRatio
        if ambRatio != None:
            (ratio, queryHits) = ambRatio
            ambPerc = "%d%%" % (ratio*100)
            if ratio >= 0.5:                        
                desc = "This combination is ambiguous and has two valid readings, -%s- or -%s-. Ambiguity Percentage: %s" % (reading1, reading2, ambPerc)
                color = "red"
            else:
                maxHit = sorted(queryHits, key=queryHits.__getitem__)[1]
                bestRead = bestReadingFinder(reading1, reading2, maxHit)
                desc = "This combination is ambiguous and has two readings, -%s- and -%s-, but the valid reading seems to be -%s-. Ambiguity Percentage: %s" % (reading1, reading2, bestRead, ambPerc)
                color = "orange"
        
            s_ind = toks.index(amb_case[0])
            e_ind = s_ind + 4
            toks.insert(s_ind, stag % (color, "analytical", desc))
            toks.insert(e_ind, etag)
            return ' '.join(toks)

    ##young men and women / real estates and vehicles"""
    elif coor_fishNet!=[]:
        for (w, t) in coor_fishNet:
            amb_case.append(w)

        q1 = "%s %s" % (amb_case[0], amb_case[1])
        q2 = "%s %s" % (amb_case[0], amb_case[3])
        reading1 = "%s %s %s %s" % (amb_case[0], amb_case[1], amb_case[2], amb_case[3])
        reading2 = "%s %s %s %s %s" % (amb_case[0], amb_case[1], amb_case[2], amb_case[0], amb_case[3])
        hits = googla(q1, q2)
        ambRatio = ambRatioEval(hits)
        print ambRatio
        if ambRatio != None:
            (ratio, queryHits) = ambRatio
            ambPerc = "%d%%" % (ratio*100)
            if ratio >= 0.5:                        
                desc = "This combination is ambiguous and has two valid readings, -%s- or -%s-. Ambiguity Percentage: %s" % (reading1, reading2, ambPerc)
                color = "red"
            else:
                maxHit = sorted(queryHits, key=queryHits.__getitem__)[1]
                bestRead = bestReadingFinder(reading1, reading2, maxHit)
                desc = "This combination is ambiguous and has two readings, -%s- and -%s-, but the valid reading seems to be -%s-. Ambiguity Percentage: %s" % (reading1, reading2, bestRead, ambPerc)
                color = "orange"

        s_ind = toks.index(amb_case[0])
        e_ind = s_ind + 5
        toks.insert(s_ind, stag % (color, "coordination", desc))
        toks.insert(e_ind, etag)
        return ' '.join(toks)      


    #I saw a boy with a telescope / I saw a tree with a telescope
    elif PPA_fishNet!=[] and PPA_fishNet[0][0] not in linkingV:
        for (w, t) in PPA_fishNet:
            if t == "IN":
                ind = PPA_fishNet.index((w, t))

        V = PPA_fishNet[0][0]
        N1 = ' '.join([w[0] for w in PPA_fishNet[1:ind]])
        PP = ' '.join([w[0] for w in PPA_fishNet[ind:]])

        q1 = V + " " + PP
        q2 = N1 + " " + PP
        hits = googla(q1, q2)
        print hits
        ambRatio = ambRatioEval(hits)
        print ambRatio
        if ambRatio != None:
            (ratio, queryHits) = ambRatio
            ambPerc = "%d%%" % (ratio*100)
            if ratio >= 0.5:                        
                desc = "Prepositional phrase can attach to both Noun and Verb like -%s- or -%s-. Ambiguity Percentage: %s" % (q1, q2, ambPerc)
                color = "red"
            else:
                maxHit = sorted(queryHits, key=queryHits.__getitem__)[1]
                desc = "Prepositional phrase can attach to both Noun and Verb like -%s- or -%s-, but the valid attachment seems to be -%s-. Ambiguity Percentage: %s" % (q1, q2, maxHit, ambPerc)
                color ="orange"            
        


        toks.insert(0, stag % (color, "attachment", desc))
        toks.insert(len(toks), etag)
        return ' '.join(toks) 

    else: return sent



def data_process(text_data):
    if text_data=="":
        return "<span style='background:; color:red'>Please enter your text in the text area</span>"
    
    else:
        sents = sent_tokenizer.tokenize(text_data)        
        results = []
        for sent in sents:
            results.append(syntactic(sent))
        return ' '.join(results)
