from h2o_wave import main, app, Q, ui, on, run_on
from typing import Optional, List
import pandas as pd

def add_card(q, name, card) -> None:
    q.client.cards.add(name)
    q.page[name] = card

def clear_cards(q, ignore: Optional[List[str]] = []) -> None:
    if not q.client.cards:
        return

    for name in q.client.cards.copy():
        if name not in ignore:
            del q.page[name]
            q.client.cards.remove(name)

# Function to generate dashboard data
def generate_dashboard_data(df):
    mean_value = df['LV ActivePower (kW)'].mean()
    median_value = df['LV ActivePower (kW)'].median()
    std_dev = df['LV ActivePower (kW)'].std()
    coef_variation = std_dev / mean_value
    return mean_value, median_value, std_dev, coef_variation

# Function to generate a chart page
async def generate_chart_page(q: Q, page_name: str, page_title: str, df: pd.DataFrame, chart_data: pd.DataFrame, x_col: str, y_col: str, summary: str):
    mean_value, median_value, std_dev, coef_variation = generate_dashboard_data(df)

    add_card(q, f'stats_{page_name}', ui.form_card(
        box='horizontal', items=[
            ui.stats([
                ui.stat(label='Mean Value', value=f'{mean_value:.2f}'),
                ui.stat(label='Median Value', value=f'{median_value:.2f}'),
                ui.stat(label='Standard Deviation', value=f'{std_dev:.2f}'),
                ui.stat(label='Coefficient Variation', value=f'{coef_variation:.2f}'),
            ]),
            ui.text_l(f"{page_title} Summary"),
            ui.text(summary)
        ]
    ))

    # Convert Timestamp to string for JSON serialization
    chart_data[x_col] = chart_data[x_col].astype(str)
    plot_data = [(row[x_col], row[y_col]) for _, row in chart_data.iterrows()]

    add_card(q, f'chart_{page_name}', ui.plot_card(
        box='vertical',
        title=page_title,
        data={
            'fields': [x_col, y_col],
            'rows': [{'x': row[0], 'y': row[1]} for row in plot_data],
        },
        plot=ui.plot([ui.mark(type='line', x='=x', y='=y')])
    ))

@on('#page1')
async def page1(q: Q):
    q.page['sidebar'].value = '#page1'
    clear_cards(q)

    # Read the CSV data
    df = pd.read_csv('data/T1.csv')
    df['Date/Time'] = pd.to_datetime(df['Date/Time'], format='%d %m %Y %H:%M')

    await generate_chart_page(q, 'page1', 'Quarterly Summary', df, df, 'Date/Time', 'LV ActivePower (kW)', 'Summary of the quarterly performance metrics.')

@on('#page2')
async def page2(q: Q):
    q.page['sidebar'].value = '#page2'
    clear_cards(q)

    # Read the CSV data
    df = pd.read_csv('data/T1.csv')
    df['Date/Time'] = pd.to_datetime(df['Date/Time'], format='%d %m %Y %H:%M')

    await generate_chart_page(q, 'page2', 'Turbine Coordinates', df, df, 'Date/Time', 'LV ActivePower (kW)', 'Coordinates and locations of turbines.')

@on('#page3')
async def page3(q: Q):
    q.page['sidebar'].value = '#page3'
    clear_cards(q)

    # Read the CSV data
    df = pd.read_csv('data/T1.csv')
    df['Date/Time'] = pd.to_datetime(df['Date/Time'], format='%d %m %Y %H:%M')

    df['Year'] = df['Date/Time'].dt.year
    yearly_data = df.groupby('Year')['LV ActivePower (kW)'].sum().reset_index()

    await generate_chart_page(q, 'page3', 'Yearly Change In Production', df, yearly_data, 'Year', 'LV ActivePower (kW)', 'Yearly change in production metrics.')

@on('#page4')
async def page4(q: Q):
    q.page['sidebar'].value = '#page4'
    clear_cards(q)

    # Read the CSV data
    df = pd.read_csv('data/T1.csv')
    df['Date/Time'] = pd.to_datetime(df['Date/Time'], format='%d %m %Y %H:%M')

    await generate_chart_page(q, 'page4', 'Mean Time To Failure By Model', df, df, 'Date/Time', 'LV ActivePower (kW)', 'Mean time to failure categorized by model.')

@on('#page5')
async def page5(q: Q):
    q.page['sidebar'].value = '#page5'
    clear_cards(q)

    # Read the CSV data
    df = pd.read_csv('data/T1.csv')
    df['Date/Time'] = pd.to_datetime(df['Date/Time'], format='%d %m %Y %H:%M')

    await generate_chart_page(q, 'page5', 'Top 3 Failures', df, df, 'Date/Time', 'LV ActivePower (kW)', 'Top 3 failures observed.')

@on('#page6')
async def page6(q: Q):
    q.page['sidebar'].value = '#page6'
    clear_cards(q)

    # Read the CSV data
    df = pd.read_csv('data/T1.csv')
    df['Date/Time'] = pd.to_datetime(df['Date/Time'], format='%d %m %Y %H:%M')

    await generate_chart_page(q, 'page6', 'Mean Time To Bearing Failure', df, df, 'Date/Time', 'LV ActivePower (kW)', 'Mean time to bearing failure metrics.')

@on('#page7')
async def page7(q: Q):
    q.page['sidebar'].value = '#page7'
    clear_cards(q)

    # Read the CSV data
    df = pd.read_csv('data/T1.csv')
    df['Date/Time'] = pd.to_datetime(df['Date/Time'], format='%d %m %Y %H:%M')

    await generate_chart_page(q, 'page7', 'Predicted Bearing Faults', df, df, 'Date/Time', 'LV ActivePower (kW)', 'Predicted bearing faults.')

async def init(q: Q) -> None:
    q.page['meta'] = ui.meta_card(box='', layouts=[ui.layout(breakpoint='xs', min_height='100vh', zones=[
        ui.zone('main', size='1', direction=ui.ZoneDirection.ROW, zones=[
            ui.zone('sidebar', size='250px'),
            ui.zone('body', zones=[
                ui.zone('header'),
                ui.zone('content', zones=[
                    ui.zone('horizontal', direction=ui.ZoneDirection.ROW),
                    ui.zone('vertical'),
                    ui.zone('grid', direction=ui.ZoneDirection.ROW, wrap='stretch', justify='center')
                ]),
            ]),
        ])
    ])])
    q.page['sidebar'] = ui.nav_card(
        box='sidebar', color='card',
        value=f'#{q.args["#"]}' if q.args['#'] else '#page1',
        image='https://www.neuralix.ai/nix-full-icon.svg', items=[
            ui.nav_group('Menu', items=[
                ui.nav_item(name='#page1', label='Quarterly Summary'),
                ui.nav_item(name='#page2', label='Turbine Coordinates'),
                ui.nav_item(name='#page3', label='Yearly Change In Production'),
                ui.nav_item(name='#page4', label='Mean Time To Failure By Model'),
                ui.nav_item(name='#page5', label='Top 3 Failures'),
                ui.nav_item(name='#page6', label='Mean Time To Bearing Failure'),
                ui.nav_item(name='#page7', label='Predicted Bearing Faults'),
            ]),
        ])
    q.page['header'] = ui.header_card(
        box='header', title='Wind Farm Dashboard', subtitle='Operational and Failure Analysis'
    )
    # If no active hash present, render page1.
    if q.args['#'] is None:
        await page1(q)

@app('/')
async def serve(q: Q):
    # Run only once per client connection.
    if not q.client.initialized:
        q.client.cards = set()
        await init(q)
        q.client.initialized = True

    # Handle routing.
    await run_on(q)
    await q.page.save()

if __name__ == '__main__':
    import os
    from werkzeug.middleware.dispatcher import DispatcherMiddleware
    from werkzeug.serving import run_simple

    # Integrate Dash app with H2O Wave app
    application = DispatcherMiddleware(app)

    run_simple('0.0.0.0', 8000, application, use_reloader=True, use_debugger=True)


