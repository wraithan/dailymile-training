var chart = document.getElementById('chart');

var data = [{'type': 'bike', 'real': 180, 'goal': 160},
            {'type': 'hike', 'real': 5, 'goal': 8},
            {'type': 'run', 'real': 15, 'goal': 15}]

var chart = document.getElementById('chart')

var maxHeight = 100
var width = 10

data.forEach(function(item) {
    var max = Math.max(item.real, item.goal)
    var real = document.createElement('div')
    real.setAttribute('class', 'real')
    real.style.height = Math.floor((item.real/(max*1.1))*maxHeight)
    real.appendChild(document.createTextNode('\u00a0'))
    chart.appendChild(real)
    var goal = document.createElement('div')
})
