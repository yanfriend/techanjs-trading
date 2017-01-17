
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
         "Holding Days": 0,
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

function find_index_for_date(feed, input_date) {
    var low=0, high=feed.length-1;
    while (low<=high) {
        var mid = Math.floor((low+high)/2);

        if (feed[mid].date === input_date) return mid;
        else if (feed[mid].date > input_date) high=mid-1;
        else low=mid+1;
    }
    return low;
}

function load_data(data_file, date_str, is_end_date) {

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


        start_date = parseDate(date_str);  // '2006-12-16'); // new Date(2010,1,1);
        start_date_index = find_index_for_date(feed, start_date);

        if (is_end_date) {
            start_date_index = start_date_index - (BEFORE_WINDOW+WINDOW) -1;
            // make sure show last bar, not ensure can play. give one more extra bar for first click.
        }

        if (start_date_index >= feed.length) {
            console.log('date selected is out of range of sybmol');
            return;
        } else if (start_date_index < 0) {
            if (is_end_date) return; // make sure end date is the last bar in slide show.
            start_date_index=0;
        }

        feed = feed.slice(start_date_index, start_date_index+BEFORE_WINDOW+WINDOW+AFTER_WINDOW);
        data = feed.slice(0, BEFORE_WINDOW+WINDOW);  // feed is for all fitted data; data is for gaming

        if (BEFORE_WINDOW+WINDOW-1 >= feed.length) init_global(feed[feed.length-1]['close']); // only for end date setting, no meaning
        else init_global(feed[BEFORE_WINDOW+WINDOW-1]['close']);

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
