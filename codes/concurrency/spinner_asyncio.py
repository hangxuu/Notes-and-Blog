import asyncio
import itertools


async def spin(msg):
    for ch in itertools.cycle('|/-\\'):
        status = ch + ' ' + msg
        # \r:将光标回退到本行的开头位置
        print(status, flush=True, end='\r')
        try:
            await asyncio.sleep(.1)
        except asyncio.CancelledError:
            print(' ' * len(status), end='\r')
            break


async def slow_function():
    await asyncio.sleep(3)
    return 42


async def supervisor():
    spinner = asyncio.create_task(spin("Thinking!"))
    print(f'spinner object: {spinner}')
    result = await slow_function()
    spinner.cancel()
    return result


def main():
    result = asyncio.run(supervisor())
    print(f"Answer: {result}")


if __name__ == "__main__":
    main()
