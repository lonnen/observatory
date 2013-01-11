var processReleases = function(releaseList){
        upcoming = [];
        for (var i = 0; i < 2; i++) {
            upcoming.push(releaseList.shift());
        }

        d3.select("#upcoming tbody")
            .selectAll("tr")
            .data(upcoming)
          .enter()
            .append("tr")
            .html(function(data) {
                data.tag = data.ref.split("v")[1];
                return Mustache.render(
                    '<td>{{tag}}</td>' +
                    '<td><a href="https://bugzilla.mozilla.org/buglist.cgi?' +
                        'query_format=advanced;target_milestone={{bugs}};' +
                        'product=Socorro;">bugs</a></td>' +
                    '<td>{{freeze}}</td>' +
                    '<td>{{release}}</td>' +
                    '<td>{{loadedOn}}</td>',
                    data);
            });

        d3.select("#releases tbody")
            .selectAll("tr")
            .data(releaseList)
          .enter()
            .append("tr")
            .html(function(data) {
                return Mustache.render(
                    '<td>{{tag}}</td>' +
                    '<td><a href="https://bugzilla.mozilla.org/buglist.cgi?' +
                        'query_format=advanced;target_milestone={{bugs}};' +
                        'product=Socorro;">bugs</a></td>' +
                    '<td>{{tag}}</td>' +
                    '<td>{{freeze}}</td>' +
                    '<td>{{release}}</td>' +
                    '<td>{{loadedOn}}</td>',
                    data);
            });
    },
    showError = function(errorMsg) {
        d3.select('#message')
            .classed('hidden', 0)
            .classed('error', 1)
            .html(errorMsg);
    };


d3.json('api/releases/', function(r) {
    if (r == null) {
        showError("Could not retrieve release information.");
        return;
    }
    processReleases(r.releases);
});
