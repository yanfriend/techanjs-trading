
function buy() {
    console.log('in buy');

    last_data = data[data.length-1];
    var last_close = last_data['close'];
    if (fund < last_close)
            return;   // not enough fund

    position = Math.floor(fund / last_close);
    fund -= position*last_close;

    entry_price = last_close;

    portfolio = 'buy';
    arrowtrades.push({date:last_data['date'], type:'buy', price:last_data['close']});
    linetrades.push({
        entry: {date: last_data['date'], type: 'buy', price: last_data['close']},
        exit: {date: last_data['date'], type: 'sell', price: last_data['close']}
    });

    row_data.push(
        {"buysell":"Buy",
         "Entry Price": entry_price.toFixed(2),
         "Exit Price": entry_price.toFixed(2),
         "Holding Days":0,
         "Gain%" : 0,
         "Max Drawdown%": 0,
         "date_index":data.length-1
        }
    );

    d3.request('http://localhost:9000/buy')
        .get(function() {} );

    d3.select("#button_next").on("click")();
}

function sell() {
    console.log('in sell');
    last_data = data[data.length-1];

    arrowtrades.push({date:last_data['date'], type:'sell', price:last_data['close']});

    var last_close = last_data['close'];
    exit_price = last_close;
    fund +=  position * last_close;
    portfolio = '';

    d3.request('http://localhost:9000/sell')
        .get(function() {} );


    d3.select("#button_next").on("click")();
}

function new_game() {
    console.log('in new game');
    //d3.request('http://localhost:9000/new_game')
    //    .get(function() {} );

    reload_or_newgame();
}


function load_data(data_file, start_index) {
    var result = d3.csv(data_file, function(error, csv) {
        feed = csv.map(function (d) {
            factor = +d['Adj Close'] / +d.Close;

            return {
                date: parseDate(d.Date),
                open: +d.Open * factor,
                high: +d.High * factor,
                low: +d.Low * factor,
                close: +d["Adj Close"],
                volume: +d.Volume  // leave it as it is so far.
            };
        }).sort(function (a, b) {
            return d3.ascending(accessor.d(a), accessor.d(b));
        });

        feed = feed.slice(start_index);
        data = feed.slice(0, BEFORE_WINDOW+WINDOW); // make it global

        init_global();

        d3.select("#button_next").on("click")();

        //arrowtrades = [
        //    { date: data[60].date, type: "buy", price: data[60].close},
        //    { date: data[100].date, type: "sell", price: data[100].close},
        //];
        //
        //linetrades = [
        //    { entry:{ date: data[60].date, type: "buy", price: data[60].close},
        //      exit: { date: data[100].date, type: "sell", price: data[100].close}
        //    },
        //];
    });
}
