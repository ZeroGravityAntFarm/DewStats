function getServers() {
    server_table = []

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", "https://stats.zgaf.io/api_v1/master", false);
    xmlHttp.onreadystatechange = function() {

        if (this.readyState == 4 && this.status == 200) {
            const servers = JSON.parse(this.response);

            for (var i = 0; i < servers["result"]["servers"].length; i++) {
                let server = servers["result"]["servers"][i];
            
                var xmlHttp = new XMLHttpRequest();

                xmlHttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                        const server_data = JSON.parse(this.response);
                        server_table.push(server_data);

                    }
                };
                xmlHttp.open("GET", "https://stats.zgaf.io/api_v1/master/" + server, false);
                xmlHttp.send();
            }

            $('#serverTable').bootstrapTable({
                data: server_table
              });

            $('#serverTable').bootstrapTable('load', server_table);

              var classes = ["table"]

            $('#serverTable').bootstrapTable('refreshOptions', {
                classes: classes.join(' ')
              })
        }
    };
    xmlHttp.send();
}