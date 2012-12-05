exports = this
courseTypeTable =
  '30': '公选'
  '21': '专选'
  '11': '专必'
  '10': '公必'
coursesFullNameTable =
  "公必": "公共必修课"
  "专必": "专业必修课"
  "公选": "公共选修课"
  "专选": "专业选修课"
  "实践": "实践课"
courseStatusTable =
  '00': '不通过'
  '01': '待筛选'
  '03': '待审核'
  '04': '待确认'
  '05': '选课成功'
  '06': '已退课'
examineTypeTable =
  '01': '笔试'
  '02': '口试'
  '03': '考查'
  '04': '操作'
  '05': '其他'
campusTable =
  '1': '男校'
  '2': '北校'
  '3': '猪海校区'
  '4': '中东'

weatherImageTable = [
  {
    key: "沙尘暴"
    url: "sanddust.jpg"
  }
  {
    key: "雨"
    url: "rain.jpg rain2.jpg"
  }
  {
    key: "雾"
    url: "mist.jpg mist2.jpg mist3.jpg"
  }
  {
    key: "阴"
    url: "overcast.jpg"
  }
  {
    key: "多云"
    url: "cloudy.jpg cloudy2.jpg cloudy3.jpg cloudy4.jpg cloudy5.jpg"
  }
  {
    key: "晴"
    url: "sun.jpg sun2.jpg sun3.jpg sun4.jpg sun5.jpg sun6.jpg sun7.jpg sun8.jpg sun9.jpg"
  }

]

currentYear = '2011-2012'
currentTerm = '1'

exports.loadingSpinner
$loadingSpinner = $('<img>').attr({
  'src': './static/img/loader.gif'
  'class': 'loading-img'
})

$lol = $('<img>').attr({
  'src': './static/img/lol.png'
  'class': 'lol-img'
})

exports.toggleLoadingScene = (selector, html, animation=no) ->
  if animation
    $(selector).empty().append(html).fadeOut(0).fadeIn()
  else
    $(selector).empty().append(html)

exports.checkRes = (res, ele) ->
  if res is "expired"
    $(ele).html("已超时，请重新登录")
    return no
  if res is "timeout"
    $(ele).html("教务系统挂了，再试一次？")
    return no
  return yes

getCourseResult = (year, term) ->
  $.ajax
    type: 'GET'
    url: '/api/course_result'
    cache: false
    data:
      year: year
      term: term


loadClassesToday = ->
  $.ajax(
    type: 'GET'
    url: '/api/timetable'
    cache: false
    data: term:currentTerm, year:currentYear
  ).done((response) ->
    #console.log response

    # borrowed from will 404
    response = response.replace /\s/g, ""
    pattern = /jc='(.*?)'.*?kcmc='(.*?)'.*?dd='(.*?)'.*?zfw='(.*?)'.*?dsz='(.*?)'.*?weekpos=([0-9])/g
    pattern.compile pattern

    classes = []
    today = new Date().getDay();
    while (result = pattern.exec response)?
      if (parseInt result[6]) == today
        classes.push result
    console.log classes

    if classes.length == 0
      toggleLoadingScene '#class-today', $lol
      return

    $tblHead = $('<thead>').append(
      $('<tr>').append(
        $('<th>').text('今日课程')
        $('<th>').text('时间')
        $('<th>').text('教室'))
    )

    $tblBody = $('<tbody>')
    for cls in classes
      $tblBody.append(
        $('<tr>').append(
          $('<td>').text(cls[2])
          $('<td>').text(cls[1])
          $('<td>').text(cls[3]))
      )

    $tbl = $('<table>')
      .attr({'class': 'table table-hover'})
      .append $tblHead, $tblBody
    toggleLoadingScene '#class-today', $tbl, yes
  )

  toggleLoadingScene '#class-today', $loadingSpinner
countDown = (end) ->
  minutes = 1000 * 60
  hours = minutes * 60
  days = hours * 24
  date = new Date()
  holidayDate = Date.parse(end)
  countDown = holidayDate - date
  if countDown / days > 0
    return Math.ceil(countDown / days)
  else
    return 0
loadWeatherToday = ->
  $.ajax
    url: "http://sou.qq.com/online/get_weather.php"
    type: "get"
    dataType: "jsonp"
    success: (data) ->
      $("#city-name").text(data.future.name)
      $("#weather").text(data.future.wea_0)
      $("#min-tem").text(data.future.tmin_0)
      $("#max-tem").text(data.future.tmax_0)
      for i in weatherImageTable
        if(data.future.wea_0.indexOf(i["key"]) > -1)
          imgs = i["url"].split(" ")
          $(".overview-bg").css("backgroundImage", "url(/static/img/weather/" + imgs[Math.floor(Math.random() * imgs.length)] + ")")
          break;
loadTips = ->
  $.getJSON("/api/tips").done (tips) ->
    for selectCourse in tips.selectCourse
      if selectCourse.status
        $("#tips").append($("<div>").addClass("alert alert-info")
                          .append($("<a>").addClass("btn btn-primary btn-large pull-right").attr("href", "/course")
                                  .html('<i class="icon-hand-right icon-white"></i> 选课'))
                          .append("<strong>正在进行选课</strong><br/>" + selectCourse.name + "选课第" + selectCourse.round + "轮筛选阶段," + selectCourse.end + "结束。"))
    $("#daysCount").text(countDown(tips.nextHoliday.start))
    $("#holidayName").attr("title", tips.nextHoliday.name + tips.nextHoliday.days + "天").tooltip();


loadCourses = ->
  $.when(getCourseResult(currentYear, currentTerm)).done (response) ->
    courses = eval("courses = " + response).body.dataStores.xsxkjgStore.rowSet.primary
    coursesCount =
      "公必": 0
      "专必": 0
      "公选": 0
      "专选": 0
      "实践": 0
    allCoursesCount = courses.length
    if courses.length is 0
      return
    for course in courses
      coursesCount[courseTypeTable[course.kclbm]]++
    for name, count of coursesCount
      if count is 0
        continue
      $("#courses").append($("<span>").addClass("badge").text(count))
                   .append(coursesFullNameTable[name] + "</br>")
    $("#courses").append($("<span>").addClass("badge badge-info").text(allCoursesCount))
                .append("所有课程")


$ ->



  # if on home page
  if $('#class-today').length
    loadClassesToday()
    loadWeatherToday()
    loadCourses()
    loadTips()

  $('.remove-class-btn').live 'click', ->
    choice = confirm '确定退课？'

    if (choice)
      $.ajax(
        type: 'GET'
        url: '/api/remove_course'
        cache: false
        data: id: $(this).val()
      ).done((response) =>
        eval('tableJson = ' + response)
        $(@).replaceWith("<span>" + "退课状态:" + tableJson.body.parameters.dataSave + "(请重新查询进行确认)" + "</span>")
      )

  # bind query available courses event
  $('.course-type-btn-group .btn').click((event) ->
    event.preventDefault()
    console.log ($ this).val()
  )

  $('.term-btn-group2 .btn').click((event) ->
    event.preventDefault()
    console.log ($ this).val()
    console.log ($ '#year').val()
    term = $(this).val()
    year = $('#year').val()

    $.when(getCourseResult(year, term)).done((response) ->
      # genetate table
      eval('tableJson = ' + response)
      courses = tableJson.body.dataStores.xsxkjgStore.rowSet.primary

      if courses.length == 0
        toggleLoadingScene '#course-result', $lol
        return

      $tblHead = $('<thead>').append(
        $('<tr>').append(
          $('<th>').html($('<span>').attr('class', 'label').text('类型'))
            .append(' 已选课程')
          $('<th>').text('学分')
          $('<th>').text('考核方式')
          $('<th>').text('筛选情况')
          $('<th>').text('退课'))
      )

      $tblBody = $('<tbody>')
      for course in courses
        $tblBody.append(
          $('<tr>').append(
            $('<th>').html($('<span>').attr('class', 'label').text(courseTypeTable[course.kclbm]))
              .append(' '+course.kcmc)
            $('<td>').text(course.xf)
            $('<td>').text(examineTypeTable[course.khfs] ?= '')
            $('<td>').text(courseStatusTable[course.xkcgbz])
            $('<td>').html($('<button>')
                             .text('退课')
                             .addClass('btn btn-danger remove-class-btn')
                             .val(course.resource_id))
          )
        )

      $tbl = $('<table>')
        .attr({'class': 'table table-condensed table-hover'})
        .append $tblHead, $tblBody
      toggleLoadingScene '#course-result', $tbl, yes
    )

    toggleLoadingScene '#course-result', $loadingSpinner
  )
