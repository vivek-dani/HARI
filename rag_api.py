import constants as cnst
import chromadb
from os.path import join
from collections import defaultdict
import json

from litellm import completion

def answer_frm_rag(query):
    client = chromadb.PersistentClient(path=cnst.rag_path)
    collection = client.get_or_create_collection(name="global")
    
    query_results = collection.query(
        query_texts=[query],
        n_results=1
    )

    ans = rag_ans(query, query_results['documents'][0][0])
    if query_results["metadatas"][0][0] and "video_name" in query_results["metadatas"][0][0]:
        return join(cnst.video_path, query_results["metadatas"][0][0]["video_name"]+".mp4"), ans

    return "", ans

def rag_ans(query, retrieved_documents):
    information = "\n\n".join(retrieved_documents)

    response = completion(
            model="gpt-4o",
            messages=[{
            "role": "system",
            "content": "You are a helpful personal assistant."
            "You will be shown the user's question, and the relevant context information. Answer the user's question using only this information."
        },
        {"role": "user", "content": f"Question: {query}. \n Information: {information}"}],
        )
    response = response.choices[0].message.content
    return response

def get_actions():
    time_dict = defaultdict(list)
    time_evidence = defaultdict(list)

    with open(cnst.action_items_file, "r", encoding="utf-8") as file:
        for line in file:
            data = json.loads(line)
            if data['Date time for reminder'] and data['Date time for reminder'] != "NA":
                time_dict[data['Date time for reminder']].append(data['Future Actionable'] + " " + data['Reason'])
                time_evidence[data['Date time for reminder']].append(data["video_name"])
    return time_dict, time_evidence