exports = this
getScore = (ctx, year, term) ->
  $.ajax
    url: "/api/score"
    context: ctx
    data:
      year: year
      term: term
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
  $.get "/api/required_credit", grade: grade, tno: tno, (res)->
    console.log(res)

getEarnedCredit = ->
  $.get "/api/earned_credit", (res)->
    console.log(res)

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
  if credit.earn_cdt == credit.req_cdt
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
                   .text(credit.earn_cdt - credit.req_cdt)))
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


genGChartUrl = (scores, type) ->
  scores = scores.join(",")
  url = "http://chart.apis.google.com/chart?chs=600x200&chd=t:#{scores}&cht=p3&chhco=ff0000&chl=<60|60-69|70-79|80-89|90-100"

getDistributedScore = (scores) ->
  ret = [['ID', '分数', '学分', '时间', '绩点']]
  for score in scores
    detail = []
    detail.push if score.jxbmc and score.kcmc then score.jxbmc + score.kcmc else score.jxbmc || score.kcmc
    detail.push parseFloat(score.zzcj)
    detail.push parseFloat(score.xf)
    detail.push score.xnd
    detail.push parseFloat(score.jd)
    ret.push detail
  ret

drawData = (data, ele) ->
  data = google.visualization.arrayToDataTable(data);
  options = 
    title: '大学成绩分布图'
    hAxis: 
      title: '分数' 
    vAxis: 
      title: '学分'
      minValue: 0
      maxValue: 7
    bubble: 
      textStyle: 
        color: 'none'
  chart = new google.visualization.BubbleChart ele;
  chart.draw data, options;
$ ->
  $.when(getRequiredCredit(), getEarnedCredit(), getGpa()).done ->
    req_cdts = eval("req_cdts = " + arguments[0][0]).body.dataStores.zxzyxfStore.rowSet.primary
    earn_cdts = eval("earn_cdts = " + arguments[1][0]).body.dataStores.xfStore.rowSet.primary
    gpas = eval("gpas = " + arguments[2][0]).body.dataStores.jdStore.rowSet.primary
    console.log credits = organizeCredits(req_cdts, earn_cdts, gpas)
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
  $("#gpa-query-btn").click ->
    toggleLoadingScene '#gpa-chart', $loadingSpinner
    getScore($("#gpa-chart")[0]).done (res) ->
      if checkRes(res, this)
        scores = eval("scores =" + res).body.dataStores.kccjStore.rowSet.primary
        distributedScore = getDistributedScore scores
        console.log distributedScore
        drawData distributedScore, this
    .fail ->
      $(this).html "请求失败，再试一次？"
  # $.when.apply($, getAllScore(2009)).done ->
  #   score_dist = [0,0,0,0,0]
  #   for res in arguments
  #     data = eval("data =" + res[0]).body.dataStores.kccjStore.rowSet.primary
  #     for score in data
  #       switch 
  #         when score.zzcj<60 then score_dist[0]++
  #         when 60<score.zzcj<69 then score_dist[1]++
  #         when 70<score.zzcj<79 then score_dist[2]++
  #         when 80<score.zzcj<89 then score_dist[3]++
  #         when 90<score.zzcj<100 then score_dist[4]++
  #       # console.log score.xnd + " " + score.xq + " " + score.kcmc + " " + score.zzcj 
  #   console.log score_dist
  #   console.log genGChartUrl(score_dist, "bing")
  #   gchart = $("<img>").attr("src", genGChartUrl(score_dist, "bing"))
  #   toggleLoadingScene("#gpa-chart", gchart, yes)
  # 