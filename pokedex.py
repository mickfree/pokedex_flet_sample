import flet as ft
import aiohttp
import asyncio

current_pokemon = 0

#Main function
async def main(page: ft.Page):
    page.window_width = 720
    page.window_height = 1280
    page.window_resizable = False
    page.padding = 0
    #define fonts
    page.fonts = {
        "zpix": "https://github.com/SolidZORO/zpix-pixel-font/releases/download/v3.1.8/zpix.ttf"
    }

    page.theme = ft.Theme(font_family="zpix")

    # Asynchronous HTTP request function
    async def request(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()
            
    # Event handler for getting Pokemon data
    async def get_pokemon_event(e: ft.ContainerTapEvent):
        global current_pokemon
        if e.control == up_arrow:
            current_pokemon += 1
        else:
            current_pokemon -= 1

        number = (current_pokemon % 150) + 1
        result = await request(f"https://pokeapi.co/api/v2/pokemon/{number}")
        data = f"Name: {result['name']}\n\nTypes:"

        for element in result['types']:
            ability = element['type']['name']
            data += f"\t{ability}"
        data += f"\nMoves: {result['moves'][0]['move']['name']}"
        data += f"\nPokédex number: {result['id']}"
        text.value = data
        sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{number}.png"
        image.src = sprite_url
        await page.update_async()

    
    # Blinking animation
    async def blink():
        while True:
            await asyncio.sleep(1)
            blue_light.bgcolor = ft.colors.RED_100
            await page.update_async()
            await asyncio.sleep(0.1)
            blue_light.bgcolor = ft.colors.BLUE
            await page.update_async()

    blue_light = ft.Container(width=70, height=70, left=5, top=4, bgcolor=ft.colors.BLUE, border_radius=50)
    # Blue button with light
    blue_button = ft.Stack([        
        ft.Container(width=80, height=80, bgcolor=ft.colors.WHITE, border_radius=50),
        blue_light
    ])

    # Top items for the interface
    top_items = [
        ft.Container(blue_button, width=80, height=80),
        ft.Container(width=40, height=40, bgcolor=ft.colors.ORANGE, border_radius=50),
        ft.Container(width=40, height=40, bgcolor=ft.colors.YELLOW, border_radius=50),
        ft.Container(width=40, height=40, bgcolor=ft.colors.GREEN, border_radius=50),
    ]
    

    black_screen = ft.Stack([
        ft.Container(width=500, height=350, right=50, top=30, bgcolor=ft.colors.BLACK),
    ])

    central_item = [
        ft.Container(black_screen, width=600, height=400, bgcolor=ft.colors.WHITE),
        ft.Image(
            src="https://github.com/PokeAPI/sprites/blob/ca5a7886c10753144e6fae3b69d45a4d42a449b4/sprites/pokemon/1.png"
        )  
    ]

    pokemon_background = ft.Stack([
        ft.Image(
            src="https://img.freepik.com/fotos-premium/cartoon-illustration-of-forest-with-waterfall-and-trees-generative-ai_900396-47718.jpg",
            left=2
        )
    ])

    sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png"

    image = ft.Image(
        sprite_url,
        scale=8,    
        width=50,
        height=50,
        top=350/2,
        right=550/2
    )

    # Create a triangle shape for the up arrow
    central_stack = ft.Stack([
        ft.Container(width=600, height=400, bgcolor=ft.colors.WHITE, border_radius=20),
        ft.Container(pokemon_background, width=550, height=350, bgcolor=ft.colors.BLACK, top=25, left=25),
        image 
    ]) 

    # Create a triangle shape for the up arrow
    triangle = ft.canvas.Canvas([
        ft.canvas.Path([
            ft.canvas.Path.MoveTo(40, 0),
            ft.canvas.Path.LineTo(0, 50),
            ft.canvas.Path.LineTo(80, 50),
        ],
        paint=ft.Paint(
            style=ft.PaintingStyle.FILL,   # Filling
        ))
    ],
    width=80,
    height=50,
    )
    # Create the container for the up arrow
    up_arrow = ft.Container(triangle, width=80, height=50, on_click=get_pokemon_event)
    # Create a column with up and down arrows
    arrows = ft.Column([
        up_arrow,  # Up arrow
        # Use rotations to invert the triangle
        ft.Container(triangle, rotate=ft.Rotate(angle=3.14159), width=80, height=50, on_click=get_pokemon_event),  # Down arrow
    ])

    # Create a text container for displaying Pokemon data
    text = ft.Text(value="... LOAD ...", color=ft.colors.YELLOW, size=22)

    bottom_item = [
        ft.Container(width=50),  # Left margin
        ft.Container(text, padding=20, width=400, height=300, bgcolor=ft.colors.GREEN, border_radius=20),  # Pokémon info
        ft.Container(width=30),  # Right margin
        ft.Container(arrows, width=80, height=120)
    ]

    # Create the main column layout

    top_container = ft.Container(content=ft.Row(top_items), width=600, height=80, margin=ft.margin.only(top=40))
    center_container = ft.Container(content=central_stack, width=600, height=400, margin=ft.margin.only(top=40), alignment=ft.alignment.center)
    bottom_container = ft.Container(content=ft.Row(bottom_item), width=600, height=250, margin=ft.margin.only(top=40))

    column = ft.Column(spacing=0, controls=[
        top_container,
        center_container,
        bottom_container,
    ])

    # Container for the entire page
    container = ft.Container(column, width=720, height=1280, bgcolor=ft.colors.RED, alignment=ft.alignment.top_center)
    # Add the container to the page and start the blinking animation
    await page.add_async(container)
    await blink()

# Start the Flet application
ft.app(target=main)
