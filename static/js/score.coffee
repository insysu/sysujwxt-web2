getScore = (year, term) ->
  $.get '/api/score',  year:year, term:term


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

drawData = (data) ->
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
  chart = new google.visualization.BubbleChart(document.getElementById('gpa-chart'));
  chart.draw data, options;
$ ->
  $("#gpa-query-btn").click ->
    getScore().done (res) ->
      scores = eval("scores =" + res).body.dataStores.kccjStore.rowSet.primary
      distributedScore = getDistributedScore scores
      console.log distributedScore
      drawData distributedScore

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