var showChart={
    href_month:["./committer_date_histogram.html","./committer_date_pie.html",
        "./author_date_histogram.html","./committer_date_pie.html",
        "../image/compare_lineChart.jpg"],
    href_login:[],
    href_hour:"./Linus_hour_commit.html",
    href_week:"./Linus_week_commit.html",
    href_message:"./message_analysis.html",
    init:function () {
        var self=this;
         $(function(){
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

         })
    },
    loadHtml:function(href){
        var $content= $("#right");
        $content.innerHTML="";
        $content.load(href);
        // $content.style.width=this.rightSection_width;
    },
    loadImage:function(href){
        var content=$("#right");
        content.empty();
        var img=document.createElement("img");
        img.src=href;
        content.append(img);
    },

};
showChart.init();

