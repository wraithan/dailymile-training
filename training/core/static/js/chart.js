var graph = function (data) {
    var chart = document.getElementById('chart')

    var derive_width = function(value, max) {
        return Math.floor((value/max)*400);
    };

    data.forEach(function(item) {
        var max = Math.max(item.real, item.goal);
        var label = document.createElement('p');
        var real = document.createElement('div');
        var goal = document.createElement('div');

        label.appendChild(document.createTextNode(item.label
                                                  + ' goal:'
                                                  + item.goal
                                                  +  ' real:'
                                                  + item.real));
        chart.appendChild(label);
        real.setAttribute('id', item + 'Bar');
        real.setAttribute('class', 'chart-real');
        real.style.width = derive_width(item.real, max) + 'px';
        label.appendChild(real);
        goal.setAttribute('class', 'chart-goal');
        goal.style.width = derive_width(item.goal, max) + 'px';
        goal.appendChild(document.createTextNode('\u00a0'));
        real.appendChild(goal);
    });
}
