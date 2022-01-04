from server import KServer
import asyncio
import sys

message_queue = asyncio.Queue()


def recv_input(loop=None):
    global message_queue
    if loop == None:
        loop = asyncio.get_event_loop()
    asyncio.ensure_future(message_queue.put(sys.stdin.readline()), loop=loop)

async def read(msg, loop=None):
    print(msg)
    
    if loop == None:
        loop = asyncio.get_event_loop()
    
    sys.stdout.flush()
    loop.add_reader(sys.stdin, recv_input)
    inp = await message_queue.get()
    loop.remove_reader(sys.stdin)
    print(inp)
    return inp



def auth_menu(kserver):

    sys.stdout.flush()
    print("[1] Register")
    print("[2] Login")

    loop = kserver.loop
    option = int(input("Option > "))
    username = input("Username: ")
    
    if option == 1:
        try:
            future = asyncio.run_coroutine_threadsafe(kserver.register(username), loop)
            return future.result()
        
        except Exception as e:
            print(e)

    elif option == 2:
        try:
            future = asyncio.run_coroutine_threadsafe(kserver.login(username), loop)
            return future.result()
        
        except Exception as e:
            print(e)

    return None


def main_menu(kserver):
    print("[1] Follow user")
    print("[2] Show followers")
    print("[3] Show following")
    print("[4] Post message")
    print("[5] Timeline")
    print("[0] Exit")
    option = int(input("option > "))
    loop = kserver.loop
    

    if option == 1:
        try:
            username = input("Username: ")
            future = asyncio.run_coroutine_threadsafe(kserver.follow_user(username), loop)
            #print(future.result())
            main_menu(kserver)
            #return future.result()
        
        except Exception as e:
            print(e)

    elif option == 2:
        kserver.node.show_followers()
        main_menu(kserver)

    elif option == 3:
        kserver.node.show_following()
        main_menu(kserver)


    elif option == 4:
        message = input("Message: ")
        future = asyncio.run_coroutine_threadsafe(kserver.save_message(message), loop)
        main_menu(kserver)
    
    elif option == 5:
        future = asyncio.run_coroutine_threadsafe(kserver.get_timeline(), loop)
        kserver.show_timeline(future.result())
        main_menu(kserver)

    elif option == 0:
        return