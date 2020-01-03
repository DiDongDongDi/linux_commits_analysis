var showChart={
    href_month:["./committer_date_histogram.html","./committer_date_pie.html",
        "./author_date_histogram.html","./committer_date_pie.html",
        "../image/compare_lineChart.jpg"],
    href_login:[],
    href_hour:"./Linus_hour_commit.html",
    href_week:"./Linus_week_commit.html",
    href_message:"./message_analysis.html",
    href_person:["./author_committer_counts.html","./author_committer_describe.html"],
    init:function () {
        var self=this;
         $(function(){
             self.initShow();
              $("#committer_histogram").click(function (e) {
                 e.preventDefault(); //阻止事件默认行为
                self.loadHtml(self.href_month[0]);
            });
            $("#committer_pie").click(function (e) {
                 e.preventDefault();
                self.loadHtml(self.href_month[1]);
            });
            $("#author_histogram").click(function (e) {
                 e.preventDefault();
                self.loadHtml(self.href_month[2]);
            });
            $("#author_pie").click(function (e) {
                 e.preventDefault();
                self.loadHtml(self.href_month[3]);
            });
            $("#compare_lineChart").click(function (e) {
                 e.preventDefault();
                self.loadImage(self.href_month[4]);
            });
            $("#hour_commit").click(function (e) {
                 e.preventDefault();
                self.loadHtml(self.href_hour);
            });
            $("#week_commit").click(function (e) {
                 e.preventDefault();
                self.loadHtml(self.href_week);
            });
            $("#message_analysis").click(function (e) {
                 e.preventDefault();
                self.loadHtml(self.href_message);
            });
            $("#person_author_commit").click(function (e) {
                 e.preventDefault();
                self.loadHtml(self.href_person[0]);
            });
              $("#person_describe").click(function (e) {
                 e.preventDefault();
                self.loadHtml(self.href_person[1]);
            });
         })
    },
    loadHtml:function(href){
        var $content= $("#right");
        $content.innerHTML="";
        $content.load(href);
    },
    loadImage:function(href){
        var content=$("#right");
        content.empty();
        var img=document.createElement("img");
        img.src=href;
        img.style="margin:15px 0 0 15px";
        content.append(img);
    },
    initShow:function () {
        this.loadHtml(this.href_month[0]);
    }

};
showChart.init();

