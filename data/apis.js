
    function buy() {
        console.log('in buy');

        var last_close = data[data.length-1]['close'];
        if (fund < last_close)
                return;   // not enough fund

        position = Math.floor(fund / last_close);
        fund = fund - position*last_close;

        entry_price = last_close;

        console.log(position);
        console.log(fund);

        d3.request('http://localhost:9000/buy')
            .get(function() {} );
    }

    function sell() {
        console.log('in sell');
        d3.request('http://localhost:9000/sell')
            .get(function() {} );
    }

    function new_game() {
        console.log('in new game');
        d3.request('http://localhost:9000/new_game')
            .get(function() {} );
    }



    function load_data(data_file) {
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

        data = feed.slice(0, 125); // make it global

        trades = [
            { date: data[60].date, type: "buy", price: data[60].close, quantity: 1000 },
            { date: data[100].date, type: "sell", price: data[100].close, quantity: 200 },
        ];

    });

    }
