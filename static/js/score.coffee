exports = this
getScore = (ctx, year, term) ->
  $.ajax
    url: "/api/score"
    context: ctx
    data:
      year: year
      term: term
getScript = (url) ->
  $.ajax
    url: url
    cache: yes
    dataType: "script"
getGpa = (year, term) ->
  $.ajax
    url: "/api/gpa"
    data:
      year: year
      term: term
getTno = ()->
  $.ajax
    url: "/api/tno",
    async: no,
    success: (res)->
      nums = eval("nums = " + res).body.parameters.result
      exports.grade = nums.split(",")[1]
      exports.tno = nums.split(",")[2]
getRequiredCredit = ()->
  if not grade? or not tno?
    getTno()
  $.get "/api/required_credit", grade: grade, tno: tno
getEarnedCredit = ->
  $.get "/api/earned_credit"
organizeCredits = (req_cdts, earn_cdts, gpas) ->
  credits = 
    "公必": {}
    "专必": {}
    "公选": {}
    "专选": {}
    "实践": {}
    "总览": 
      "req_cdt": 0
      "earn_cdt": 0
      "gpa": 0
  for req_cdt in req_cdts
    credits[req_cdt.oneColumn[0..1]]["req_cdt"] = parseInt(req_cdt.twoColumn)
    credits["总览"]["req_cdt"] += parseInt(req_cdt.twoColumn)
  for earn_cdt in earn_cdts
    credits[earn_cdt.oneColumn[0..1]]["earn_cdt"] = parseInt(earn_cdt.twoColumn)
    credits["总览"]["earn_cdt"] += parseInt(earn_cdt.twoColumn)
  for gpa in gpas
    credits[gpa.oneColumn[0..1]]["gpa"] = parseFloat(gpa.twoColumn)
    gpaWeight = parseFloat(gpa.twoColumn) * credits[gpa.oneColumn[0..1]]["earn_cdt"]
    credits["总览"]["gpa"] += gpaWeight
  credits["总览"]["gpa"] /= credits["总览"]["earn_cdt"] 
  credits["总览"]["gpa"] = credits["总览"]["gpa"].toFixed(3)

  #calculate required credits for now. Extra earned credits cannot be summed in.
  allRequiredCreditsForNow = 0
  for key of credits
    if key is "总览" or not credits[key]["req_cdt"] 
      break
    else 
      credits[key]["req_cdt_now"] = if credits[key]["earn_cdt"] >= credits[key]["req_cdt"] then 0 else credits[key]["earn_cdt"] - credits[key]["req_cdt"]
      allRequiredCreditsForNow += credits[key]["req_cdt_now"]
  credits["总览"]["req_cdt_now"] = allRequiredCreditsForNow

  return credits
genCreditRow = (credit, rowName) ->
  if not credit.gpa? or not credit.req_cdt? or not credit.earn_cdt?
    return
  maxWidth = 420;
  maxCredit = 100;
  successTd = '<td><span class="label label-success"><i class="icon-ok icon-white"></i></span></td>'
  tr = $("<tr>")
  tr.append($("<th>").text(rowName))
  tr.append($("<td>").text(credit.gpa))
  tr.append($("<td>").text(credit.earn_cdt + "/" + credit.req_cdt))
  if credit.req_cdt_now is 0
    tr.append(successTd)
    tr.append(
      $("<td>").append(
         $("<div>").addClass("progress")
                   .addClass("progress-striped")
                   .data("length",  if (length = credit.req_cdt / maxCredit * maxWidth) > maxWidth then maxWidth else length)
                   .width(0)
                   .append(     
                     $("<div>").addClass("bar")
                               .addClass("bar-success")
                               .data("length", credit.earn_cdt / credit.req_cdt * 100 + "%")))).width(0)
  else
    tr.append(
      $("<td>").append(
        $("<span>").addClass("label")
                   .text(credit.req_cdt_now)))
    tr.append(
      $("<td>").append(
         $("<div>").addClass("progress")
                   .addClass("progress-striped")
                   .data("length",  if (length = credit.req_cdt / maxCredit * maxWidth) > maxWidth then maxWidth else length)
                   .width(0)
                   .append(     
                     $("<div>").addClass("bar")
                               .data("length", credit.earn_cdt / credit.req_cdt * 100 + "%")))).width(0)
    return tr
calculateGpa = (scores) ->
  gpaWeight = 0
  totalCredits = 0
  for score in scores
    gpaWeight += parseFloat(score.jd) * parseInt(score.xf)
    totalCredits += parseInt score.xf
  gpa = (gpaWeight / totalCredits).toFixed(3)
  $("#gpa_origin").text(gpa)

  # for 4.0
  gpaWeight = 0
  for score in scores
    zzcj = Math.round score.zzcj
    if 85 <= zzcj <= 100 
      zzcj = 4.0
    else if 80 <= zzcj <= 84
      zzcj = 3.5
    else if 75 <= zzcj <= 79
      zzcj = 3.0
    else if 70 <= zzcj <= 74
      zzcj = 2.5
    else if 65 <= zzcj <= 69
      zzcj = 2.0
    else if 60 <= zzcj <= 64
      zzcj = 1.5
    else if zzcj < 60
      zzcj = 1.0
    gpaWeight += zzcj * parseInt(score.xf)
  gpa = (gpaWeight / totalCredits).toFixed(3)
  $("#gpa_new").text(gpa)
genGChartUrl = (scores, type) ->
  scores = scores.join(",")
  url = "http://chart.apis.google.com/chart?chs=600x200&chd=t:#{scores}&cht=p3&chhco=ff0000&chl=<60|60-69|70-79|80-89|90-100"
formatScoreForBar = (scores) ->
  map = {}
  data = []
  for score in scores
    if not map[score.xnd] 
      map[score.xnd] = [0,0,0,0,0]
  for score in scores
    count = 1
    for i in [60...100] by 10
      if i <= score.zzcj < i + 10  
        map[score.xnd][count]++ 
        break
      if i > score.zzcj 
        map[score.xnd][0]++
      count++
    if parseInt(score.zzcj) is 100
      map[score.xnd][count - 1]++  
  j = 0
  for key of map
    data[j] = 
      name: key
      data: map[key]
    j++
  data.sort((a, b)->
    return a.name < b.name
    )
formatScoreForPie = (scores) ->
  data = [["<60", 0]];
  for i in [60...100] by 5
    if (i == 95)
      data.push [i + "-" + (i + 5), 0]
    else
      data.push [i + "-" + (i + 4), 0]
  
  #data = [["<60", 0], ["60-64", 0], ["65-69", 0], ["70-74", 0], ["75-79", 0], ["80-84", 0], ["85-89", 0], ["90-94", 0], ["95-100", 0]]
  for score in scores
    count = 1
    for i in [60...100] by 5
      if i <= score.zzcj < i + 5  
        data[count][1]++ 
        break
      if i > score.zzcj 
        data[0][1]++
      count++
    if parseInt(score.zzcj) is 100
      data[count - 1][1]++
  return data
drawChart = (scores, type, ele) ->
  switch type
    when 'pie' then drawPieChart(scores, ele)
    when 'bar' then drawBarChart(scores, ele)
    when 'bubble' then drawBubbleChart(scores, ele)
drawPieChart = (scores, ele) ->

  chart = new Highcharts.Chart(
            chart:
              renderTo: ele
              plotBackgroundColor: null
              plotBorderWidth: null
              plotShadow: false
            title:
              text: '大学成绩分布图'
            credits:
              href: 'http://sysujwxt.com'
              text: '中大第三方教务系统'
            tooltip:
              pointFormat: '{series.name}: <b>{point.y}</b>'
              percentageDecimals: 1
            
            plotOptions:
                pie:
                    allowPointSelect: true
                    cursor: 'pointer'
                    showInLegend: true
                    dataLabels:
                        enabled: true
                        color: '#000000'
                        connectorColor: '#000000'
                        formatter: -> 
                            '<b>'+ this.point.name + '</b>: ' + this.percentage.toFixed(2) + ' %';
            series:[
              type: "pie"
              name: "科目数量"
              data: formatScoreForPie(scores)
            ]
  );
drawBarChart = (scores, ele) ->
  chart = new Highcharts.Chart(
            chart:
                renderTo: ele
                type: 'column'
            credits:
              href: 'http://sysujwxt.com'
              text: '中大第三方教务系统'
            title:
                text: '大学成绩分布图'
            xAxis: 
                categories: ['<60', '60-70', "70-80","80-90","90-100"]
            yAxis: 
                min: 0
                title: 
                    text: '科目数量'
                stackLabels: 
                    enabled: true
                    style:
                        fontWeight: 'bold'
                        color: (Highcharts.theme and Highcharts.theme.textColor) or 'gray'
                    
            legend: 
                backgroundColor: '#FFFFFF'
                reversed: true
            tooltip: 
                formatter: ->
                    return '' + this.series.name + '学年: ' + this.y + ''; 
            plotOptions: 
                column: 
                    stacking: 'normal'
                    dataLabels: 
                        enabled: true
                        color: (Highcharts.theme and Highcharts.theme.dataLabelsColor) or 'white'
            series: formatScoreForBar(scores)
        );
$ ->

  $.when(getRequiredCredit(), getEarnedCredit(), getGpa()).done ->
    req_cdts = eval("req_cdts = " + arguments[0][0]).body.dataStores.zxzyxfStore.rowSet.primary
    earn_cdts = eval("earn_cdts = " + arguments[1][0]).body.dataStores.xfStore.rowSet.primary
    gpas = eval("gpas = " + arguments[2][0]).body.dataStores.jdStore.rowSet.primary
    credits = organizeCredits(req_cdts, earn_cdts, gpas)
    tbody = $("<tbody>")
    for rowName in ["公必", "专必", "专选", "公选", "实践", "总览"]
      tbody.append(genCreditRow(credits[rowName], rowName))
    $("#credit-chart").append tbody

    #for bar animation
    delay = (ms, func) -> setTimeout func, ms
    delay 10, -> $("#credit-chart").find("div").each ->
        $(this).width($(this).data("length"))
    # -----------------------
  # bind query score event
  # -----------------------
  $('.term-btn-group .btn').click((event) ->
    term = $(this).val()
    year = $('#year').val()
    toggleLoadingScene '#score-result', $loadingSpinner
    getScore($("#score-result")[0], year, term).done((res) ->
      checkRes res, this
      # genetate table
      scores = eval('tableJson = ' + res).body.dataStores.kccjStore.rowSet.primary
      if scores.length is 0
        toggleLoadingScene this, $lol
        return
      $tblHead = $('<thead>').append(
        $('<tr>').append(
          $('<th>').html($('<span>').attr('class', 'label').text('类型'))
                   .append(' 课程')
          $('<th>').text('学分')
          $('<th>').text('成绩')
          $('<th>').text('绩点')
          $('<th>').text('教学班排名'))
      )

      $tblBody = $('<tbody>')
      for score in scores
        $tblBody.append(
          $('<tr>').append(
            $('<th>').html($('<span>').attr('class', 'label').text(courseTypeTable[score.kclb]))
              .append(' '+score.kcmc)
            $('<td>').text(score.xf)
            $('<td>').text(score.zzcj)
            $('<td>').text(score.jd)
            $('<td>').text(score.jxbpm))
        )
      
      $tbl = $('<table>')
        .attr({'class': 'table table-condensed table-hover'})
        .append $tblHead, $tblBody
      toggleLoadingScene this, $tbl, yes
    ).fail ->
      $(this).html "请求失败，再试一次？"
  )
  $(".chart-type-btn-group .btn").click (e)->
    e.preventDefault();
    toggleLoadingScene '#gpa-chart', $loadingSpinner
    type = $(this).val()
    getScore($("#gpa-chart")[0]).done (res) ->
      if checkRes(res, this)
        scores = eval("scores =" + res).body.dataStores.kccjStore.rowSet.primary
        calculateGpa(scores)
        drawChart(scores, type, this)
    .fail ->
      toggleLoadingScene this, $lol
  $(".chart-type-btn-group button[value=pie]").click()
  $("[rel=tooltip]").tooltip(
    trigger:'click'
  )
