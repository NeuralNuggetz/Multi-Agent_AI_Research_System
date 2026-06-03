from agents import build_search_agent, build_reader_agent, writer, critic_chain

def run_research_pipeline(topic : str) -> dict:
    state = {}

    # search agent working
    print("\n"+" ="*50)
    print("step 1 - search agent is working ...")
    print("="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke( {
        "messages": [("user", f"Find recent, reliable and detailded information about : {topic}")]
    })
    state["search_result"] = search_result["messages"][-1].content

    print("\n search result", state["search_result"])


    #step - 2 reader agent
    print("\n"+"="*50)
    print("step 2 - Reader agent is scraping top resources ..")
    print("="*50)

    reader_agent = build_reader_agent()
    reader_agent.invoke(
        {
            
        }
    )