<script>

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

    function reload_or_newgame() {
        console.log('load game info, open positions, or available fund, etc.');
        d3.request('http://localhost:9000/reload_or_newgame')
            .get(function(d) {
                console.log(d);
                mydict = JSON.parse(d.responseText);

                fund = mydict.fund;  // suppose global
                symbol = mydict.symbol;

                console.log(mydict);
            } );
    }
    window.onload = reload_or_newgame;

    </script>
