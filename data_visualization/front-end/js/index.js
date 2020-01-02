var showList={
    dataJson:null,
    searchName:null,
    currentPage:1,
    totalPage:252,
    totalNum:2520,
    nextPageEle:null,
    previousPageEle:null,
    lastPageEle:null,
    goEle:null,
    init:function () {
        var self=this;
        $.post("../../json/users.json").done(function (data) {
            self.dataJson=JSON.parse(data);
            self.initEle();
            self.show();
        });
    },
    initEle:function(){
        var self=this;
        $(function(){
            $("#previousPage").click(function () {
                self.handlePreviousPage();
            });
            $("#lastPage").click(function () {
                self.handleLastPage();
            });
            $("#go").click(function () {
                var value=$("input#turnToPage").val();
                console.log(value);
                if(value.trim().length!==0&&!isNaN(parseInt(value))){
                     self.handleGo(value);
                }
            });
            $("#nextPage").click(function(){
                self.handleNextPage();
              });

        });
    },
    handleLastPage:function(){
      this.currentPage=this.totalPage;
      this.show();
    },
    handleGo:function(value){
        console.log("go");
        this.currentPage=parseInt(value);
        this.isPageLegal();
        this.show();
    },
    handlePreviousPage:function(){
        this.currentPage-=1;
        this.isPageLegal();
        this.show();
    },
    handleNextPage:function(){
        this.currentPage+=1;
        this.isPageLegal();
        this.show();
    },
    isPageLegal:function(){
        if(this.currentPage<1){
            this.currentPage=1;
        }
        if(this.currentPage>this.totalPage){
            this.currentPage=this.totalPage;
        }
    },
    show:function () {
        var self=this;
        var remoteDataset={
                currentPage:self.currentPage,
                totalNum: self.totalNum,
                totalPage: self.totalPage,
            };
        console.log(this.dataJson);
        var t={
            content:self.dataJson,
            remoteDataset:remoteDataset,
            };
        var html = template('rankList', t);
        document.getElementById('template_area').innerHTML = html;
    }
};
    showList.init();