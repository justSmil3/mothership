import os
from openai import OpenAI
import psycopg2
import uuid
from dotenv import load_dotenv, dotenv_values
from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.providers.anthropic import AnthropicProvider
from pydantic import BaseModel
import json
import marko

class instruction(BaseModel):
    command: str
    args: list[str]

class sturctue(BaseModel):
    summary: str
    instruction: instruction

def refin(e):
    result = ""
    if isinstance(e, list):
        for i in e:
            result += refin(i.children)
    else:
        result += e + '\n'
    return result

def research_md_file(path):
    name = path.split('/')[-1].split('\\')[0]
    env_vars = dotenv_values(".env")
    model = AnthropicModel("claude-3-5-sonnet-latest", provider=AnthropicProvider(api_key=env_vars.get("ANTHROPIC_API_KEY")))
    agent = Agent(
            model=model,
            system_prompt="you are an worker who receives a markdown file and extracts relevant information from it",
            )
    with open(path, 'r', encoding="utf-8") as f:
        markdown_content = f.read()
    markdown_content = marko.parse(markdown_content)

    description = ""
    commands = ""
    
    extract = True
    extract_docker = False
    for idx, element in enumerate(markdown_content.children):
        if isinstance(element, marko.block.BlankLine):
            continue
        if isinstance(element, marko.block.Heading):
            if "tools" in element.children[0].children.lower():
                extract = True
                continue
            if "Claude" in element.children[0].children or "docker" in element.children[0].children.lower():
                extract = True
                extract_docker = True
                continue
            if idx == 0:
                continue
            extract = False
            extract_docker = False
            continue
            
        if not extract:
            continue
        if extract_docker:
            if isinstance(element, marko.block.FencedCode) and "docker" in element.children[0].children:
                commands += element.children[0].children
            continue
        fin = element.children
        description += refin(fin)

    name += ".txt"
    print("................................")
    if len(commands) == 0:
        return
    while commands[-1] != '}':
        commands = commands[:-1]
        if len(commands) == 0:
            return
    #prompt = f"the following text is wrong json. turn it into real json and return it as json: {commands}"
    #results = agent.run_sync(prompt)
    #commands_json = json.loads(results.data)
    #data = commands_json["mcpServers"]
    #print(data)
    #for key, value in data.items():
    value = description 
    with open(os.path.join("./mcp_servers/", name), 'w', encoding="utf-8") as f:
        json.dump(value, f, indent=2, ensure_ascii=False)
    #return
    # print(description)
    return 
    exit()
    prompt = """
    The following text is a Readme file from a Model Context Protocol tool: {content}

    write a summary of all the functionality of the tool.
    additionally the readme file contains a instruction of how to run it using docker. extract it.
    """

    inst = prompt.format(content=markdown_content)
    result = agent.run_sync(prompt)
    print(result)
    with open("test.json", 'w', encoding="utf-8") as f:
        json.dump(result.data.model_dump(), f, indent=2, ensure_ascii=False)


def prep_tools():
    for rroot, dirs, _ in os.walk("./servers/src/"):
        for dir in dirs:
            for root, _, files in os.walk(os.path.join(rroot,dir)):
                for file in files:
                    if file == "README.md":
                        research_md_file(os.path.join(root, file))
    
def main():
    load_dotenv()
    client = OpenAI()
    conn = psycopg2.connect("dbname=toolnamestore user=chris password=1234 host=localhost port=5433")
    cur = conn.cursor()
    registered_files = []

    
    cur.execute("ALTER TABLE items ADD COLUMN description TEXT;")
    cur.execute("CREATE TEMP TABLE tmp (name TEXT, description TEXT);")
    
    
    for root, _, files in os.walk("./mcp_servers/"):
        for file in files:
            name = file.split('.')[0]
            if name in registered_files:
                continue
            registered_files.append(name)
            path = f"{root}{name}"
            txt_path = path + ".txt"
            json_path = path + ".json"
            with open(txt_path, "r") as f:
                description = f.read()
            with open(json_path, "r") as f:
                config = f.read()

            #response = client.embeddings.create(
            #    input=description,
            #    model="text-embedding-3-small"
            #)
            #embedding = response.data[0].embedding
            
            #id = str(uuid.uuid4())
            #print(config)
            cur.execute(
                "INSERT INTO tmp (name, description) VALUES (%s, %s)",
                (name, description)
            )

    cur.execute(
            "UPDATE items SET description = tmp.description FROM tmp WHERE items.name = tmp.name;"
            )

    cur.execute("SELECT name, description FROM items;")
    rows = cur.fetchall()
    for row in rows:
        name, description = row
        print(f'Name: {name}, Description: {description}')
    conn.commit()
    cur.close()
    conn.close()
           
def search():
    load_dotenv()
    client = OpenAI()
    query = "search through Github for a repository that collects a multitude of mcp tools"
    response = client.embeddings.create(
            input=query,
            model="text-embedding-3-small"
            )
    embedding = response.data[0].embedding
    conn = psycopg2.connect(
            dbname="toolnamestore",
            user="chris",
            password="1234",
            host="localhost",
            port="5433"
            )
    cur = conn.cursor()

    sql_query="""
    SELECT name
    FROM items
    ORDER BY embedding <#> %s
    LIMIT 2;
    """
    sql_embedding = f"[{', '. join(map(str, embedding))}]"
    cur.execute(sql_query, (sql_embedding,))
    results = cur.fetchall()
    for row in results:
        print("name:", row[0])
    cur.close()
    conn.close()

if __name__ == "__main__":
    # research_md_file("./servers/src/memory/README.md")
    # prep_tools()
    main()
