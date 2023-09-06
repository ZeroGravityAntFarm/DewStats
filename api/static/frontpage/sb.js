function getServers() {
    server_table = []

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", "http://master.zgaf.io/list", false);
    xmlHttp.onreadystatechange = function() {

        if (this.readyState == 4 && this.status == 200) {
            const servers = JSON.parse(this.response);
            console.log(servers["result"]["servers"]);

            for (var i = 0; i < servers["result"]["servers"].length; i++) {
                let server = servers["result"]["servers"][i];
                console.log("http://" + server)
            
                var xmlHttp = new XMLHttpRequest();

                xmlHttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                        const server_data = JSON.parse(this.response);
                        server_table.push(server_data);

                    }
                };
                xmlHttp.open("GET", "http://" + server, false);
                xmlHttp.send();
            }
            console.log(server_table)
            $('#serverTable').bootstrapTable({
                data: server_table
              });

              var classes = ["table"]

              $('#serverTable').bootstrapTable('refreshOptions', {
                classes: classes.join(' ')
              })
        }
    };
    xmlHttp.send();
}