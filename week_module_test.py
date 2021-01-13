import pymysql
conn = pymysql.connect(host='172.17.0.2', user='root',password='',port=3306, database='module_test',charset='utf8')
cursor = conn.cursor(pymysql.cursors.DictCursor)

#메인페이지를 위한 클래스
class module:
    #생성자
    def __init__(self):
        self.id=''
        self.pwd=''
        self.main()
    #메인 함수
    def main(self):
        print('#'*5,'Main','#'*5)
        print('1. 로그인')
        print('2. 회원가입')
        print('3. 종료')
        selectMenu = input('번호를 입력해주세요 : ') 
        
        if selectMenu == '1':
            self.login()
        
        elif selectMenu == '2':
            self.singUp()
            
        elif selectMenu == '3':
            cursor.close()
            conn.close()
            exit()
        else:
            print('다시한번 확인하세요\n')
            self.main()
    #로그인 함수
    def login(self):
        print('#'*5,'Login','#'*5)
        id = input("아이디: ")
        pwd = input('비밀번호 : ')
        sql = 'select id from member where id=%s and pwd=%s'
        cursor.execute(sql,(id,pwd))
        row = cursor.fetchone()
        if row == None:
            print('로그인에 실패하였습니다.\n')
            self.main()
        else:
            if id=='admin':
                adminClass()
            else:
                normalClass(id)
    #회원가입 함수
    def singUp(self):
        print('#'*5,'회원가입','#'*5)
        id = input('아이디를 입력하세요 : ')
        pwd = input('비밀번호를 입력하세요 : ')
        name = input('이름을 입력하세요 : ')
        email = input('이메일을 입력하세요 : ')
        sql = 'insert into member(id,pwd,name,email,created_at) values(%s,%s,%s,%s,now())'
        try:
            cursor.execute(sql,(id,pwd,name,email))
        except:
            print('회원가입에 실패했습니다. 초기메뉴로 이동합니다.\n')
            self.main()
        else:
            print('회원가입에 성고하였습니다.\n')
            conn.commit()
            self.main()
        
#관리자에 관련된 함수를 모아둔 클래스
class adminClass:
    #생성자
    def __init__(self):
        print('#'*5+'어드민 페이지'+'#'*5)
        self.adminPage()
    
    #상품관리를 위한 함수
    def manageItems(self):
            print('1. 상품 등록')
            print('2. 상품 수정')
            print('3. 상품 삭제')
            print('4. 뒤로')
            selectMode = input('메뉴를 선택해주세요 : ')
            
            if selectMode == '1':
                product_name=input('상품명을 입력하세요 : ')
                product_price = int(input('상품의 가격을 입력하세요 : '))
                product_qty = int(input('상품의 개수를 입력하세요 : '))
                sql = 'insert into item(product_name,product_price,product_qty,created_at) values(%s,%s,%s,now())'
                try:
                    cursor.execute(sql,(product_name,product_price,product_qty))
                except:
                    print('상품등록에 실패하였습니다.\n')
                else:
                    conn.commit()
                    print('상품이 등록되었습니다다.\n')
                    self.itemAll()
                finally:
                    self.manageItems()
            elif selectMode == '2':
                self.itemAll()
                selectItem = input('원하는 상품의 ID를 입력하세요 : ')
                try:
                    sql = 'select product_name,product_price,product_qty from item where id='+selectItem
                    cursor.execute(sql)
                    row = cursor.fetchone()
                    product_rename = input('수정할 상품명을 입력하세요(없을시 공란) : ')
                    product_reprice = input('수정할 상품의 가격을 입력하세요(없을시 공란) : ')
                    product_reqty = input('수정할 상품의 개수를 입력하세요(없을시 공란) : ')
                    sql = 'update item set product_name=%s,product_price=%s,product_qty = %s where id='+selectItem
                    cursor.execute(sql,(product_rename if product_rename != '' else row['product_name'], int(product_reprice) if product_reprice != '' else int(row['product_price']), int(product_reqty) if product_reqty!='' else int(row['product_qty'])))
                except:
                    print('수정에 실패하였습니다.\n')
                else:
                    conn.commit()
                    print('수정 완료되었습니다.\n')
                    self.itemAll()
                finally:
                    self.manageItems()
            elif selectMode == '3':
                self.itemAll()
                deleteItem = input('삭제할 상품을 고르세요 : ')
                try:
                    sql = 'delete from item where id='+deleteItem
                    cursor.execute(sql)
                except:
                    print('삭제에 실패하였습니다\n')
                else:
                    conn.commit()
                    print('삭제 완료하였습니다.\n')
                finally:
                    self.manageItems()
            elif selectMode == '4':
                self.adminPage()
            else:
                print('메뉴를 확인해주세요.\n')
                self.manageItems()
    #전체 상품 출력을 위한 함수
    def itemAll(self):
        sql = 'select id,product_name,product_price,product_qty,created_at from item'
        cursor.execute(sql)
        rows = cursor.fetchall()
        if len(rows) == 0:
            print('물품이 존재하지 않습니다.\n')
            self.adminPage()
        else:
            print("{:<3}\t{:<20}\t\t{:<20}\t{:<4}\t{}".format('ID','상품명','가격','수량','등록 날짜'))
            for row in rows:
                print("{:<3}\t{:<20}\t\t{:<20,}원\t{:<4}\t{}".format(row['id'],row['product_name'],row['product_price'],row['product_qty'],row['created_at']))
   
    #가입한 유저를 출력하기 위한 함수
    def memberAll(self):
        sql = 'select id,name,email,created_at from member'
        cursor.execute(sql)
        rows = cursor.fetchall()
        if len(rows) == 0:
            print('가입한 회원이 존재하지 않습니다.\n')
            self.adminPage()
        else:
            print("{:<10}\t{:<10}\t{:<30}\t{}".format('ID','이름','이메일','가입 날짜'))
            for row in rows:
                print("{:<10}\t{:<10}\t{:<30}\t{}".format(row['id'],row['name'],row['email'],row['created_at']))
   
    #모든 주문내역을 출력하기 위한 함수
    def OrdersAll(self):
        sql = 'select id,member_id,item_id,order_price,order_qty,created_at from orders'
        cursor.execute(sql)
        rows = cursor.fetchall()
        if len(rows) == 0:
            print('주문 내역이 존재하지 않습니다.\n')
            self.adminPage()
        else:
            print("{:<20}{:<20}{:<20}{:<20}{:<20}{}".format('Order Id','Member Id','Purchase Id','Product Price','Product Quantity','Date'))
            for row in rows:
                print("{:<20}{:<20}{:<20}{:<20,}{:<20}{}".format(row['id'],row['member_id'],row['item_id'],row['order_price'],row['order_qty'],row['created_at']))
   
    #특정 유저의 주문내역을 출력하기 위한 함수
    def OrdersMemberId(self):
        sql = 'select * from orders where member_id=%s'
        userId = input('원하는 유저의 아이디를 입력하세요 : ')
        cursor.execute(sql,(userId))
        rows = cursor.fetchall()
        if len(rows)==0:
            print('다시한번 확인하시기 바랍니다.\n')
        else:
            print('{:<20}{:<20}{:<20}{:<20}{:<20}{:<20}{}'.format('ID','USER ID','PRODUCT ID','PRODUCT NAME','PRICE','QUANTITY','DATE'))
            for row in rows:
                print('{:<20}{:<20}{:<20}{:<20}{:<20,}{:<20,}{}'.format(row['id'],row['member_id'],row['item_id'],row['item_name'],row['order_price'],row['order_qty'],row['created_at']))
	    
        self.adminPage()

    #최근 1주일간 가장 큰 금액을 구매한 유저를 출력하기 위한 함수
    def weeklyMember(self):
        sql = "SELECT count(*) as 'Purchase',sum(order_price) as 'Total Price',member_id from orders where date_format(created_at,'%Y-%m-%d') between date_format(date_add(now(),interval -7 day),'%Y-%m-%d') and date_format(now(),'%Y-%m-%d') group by member_id order by 'Purchase' desc"
        cursor.execute(sql)
        rows = cursor.fetchall()
        if len(rows)==0:
            print('근 1주일간 구매내역이 없습니다.\n')
        else:
            print('{:<20}{:<20}{}'.format('Purchase','Total Price','Member Id'))
            for row in rows:
                print('{:<20}{:<20,}{}'.format(row['Purchase'],row['Total Price'],row['member_id']))
        self.adminPage()

    #최근 1달간 가장 큰 금액을 구매한 유저를 출력하기 위한 함수
    def monthlyMember(self):
        sql = "SELECT count(*) as 'Purchase',sum(order_price) as 'Total Price',member_id from orders where date_format(created_at,'%Y-%m-%d') between date_format(date_add(now(),interval -1 month),'%Y-%m-%d') and date_format(now(),'%Y-%m-%d') group by member_id order by 'Purchase' desc"
        cursor.execute(sql)
        rows = cursor.fetchall()
        if len(rows)==0:
            print('근 1달간 구매내역이 없습니다.\n')
        else:
            print('{:<20}{:<20}{}'.format('Purchase','Total Price','Member Id'))
            for row in rows:
                print('{:<20}{:<20,}{}'.format(row['Purchase'],row['Total Price'],row['member_id']))
        self.adminPage()

    #최근 1주일간 주문 내역이 가장 많은 제품의 순위별로 출력하기 위한 함수
    def weeklyItem(self):
        sql = "SELECT count(*) as 'Purchase',sum(order_qty) as 'Total Quantity',item_name from orders where date_format(created_at,'%Y-%m-%d') between date_format(date_add(now(),interval -7 day),'%Y-%m-%d') and date_format(now(),'%Y-%m-%d') group by item_name order by count(*) desc,item_name asc"
        cursor.execute(sql)
        rows = cursor.fetchall()
        if len(rows)==0:
            print('근 1주일간 구매내역이 없습니다.\n')
        else:
            print('{:<20}{:<20}{}'.format('Purchase','Total Quantity','Product Name'))
            for row in rows:
                print('{:<20}{:<20,}{}'.format(row['Purchase'],row['Total Quantity'],row['item_name']))
        self.adminPage()
   
    #최근 1달간 주문 내역이 가장 많은 제품의 순위별로 출력하기 위한 함수
    def monthlyItem(self):
        sql = "SELECT count(*) as 'Purchase',sum(order_qty) as 'Total Quantity',item_name from orders where date_format(created_at,'%Y-%m-%d') between date_format(date_add(now(),interval -1 month),'%Y-%m-%d') and date_format(now(),'%Y-%m-%d') group by item_name order by count(*) desc,item_name asc"
        cursor.execute(sql)
        rows = cursor.fetchall()
        if len(rows)==0:
            print('근 1달간 구매내역이 없습니다.\n')
        else:
            print('{:<20}{:<20}{}'.format('Purchase','Total Quantity','Product Name'))
            for row in rows:
                print('{:<20}{:<20,}{}'.format(row['Purchase'],row['Total Quantity'],row['item_name']))
        self.adminPage()
        
    #관리자 페이지의 메인 함수
    def adminPage(self):
        print('0. 상품관리')
        print('1. 전체 상품 목록')
        print('2. 전체 회원 목록')
        print('3. 전체 주문 목록')
        print('4. 회원별 주문 목록')
        print('5. 주별 누적 구매액 순위')
        print('6. 월별 누적 구매액 순위')
        print('7. 주별 인기 상품 순위')
        print('8. 월별 인기 상품 순위')
        print('9. 로그아웃')
        
        selectMenu = input('메뉴를 선택하세요 : ')
        
        if selectMenu == '0':
            self.manageItems()
        elif selectMenu == '1':
            self.itemAll()
            self.adminPage()
        elif selectMenu == '2':
            self.memberAll()
            self.adminPage()
        elif selectMenu == '3':
            self.OrdersAll()
            self.adminPage()
        elif selectMenu == '4':
            self.OrdersMemberId()
        elif selectMenu == '5':
            self.weeklyMember()
        elif selectMenu == '6':
            self.monthlyMember()
        elif selectMenu == '7':
            self.weeklyItem()
        elif selectMenu == '8':
            self.monthlyItem()
        elif selectMenu == '9':
            module()
        else:
            print('메뉴를 확인해주세요.\n')
            self.adminPage()

#일반 유저를 위한 클래스
class normalClass:
    #생성자
    def __init__(self,id):
        self.id = id
        print('#'*5+self.id+'님 환영합니다'+'#'*5)
        self.userPage()

    #회원 개인 정보를 수정하기 위한 함수
    def updateInfo(self):
        print('0. 정보 보기')
        print('1. 정보 수정')
        print('2. 회원 탈퇴')
        print('3. 뒤로')

        selectMode = input('메뉴를 선택해주세요 : ')

        if selectMode == '0':
            sql = "select id,name,pwd,email from member where id=\'"+self.id+"'"
            cursor.execute(sql)
            row = cursor.fetchone()
            for k,v in row.items():
                print('{}\t: {}'.format(k,v))
            self.updateInfo()
        elif selectMode == '1':
            sql = "select pwd,email from member where id=\'"+self.id+"'"
            cursor.execute(sql)
            row = cursor.fetchone()
            pwd = input('변경할 비밀번호를 입력해주세요(원하지 않을시 공란) : ')
            email = input('변경할 이메일을 입력해주세요(원하지 않을시 공란) : ')
            try:
                sql = 'update member set pwd=%s, email=%s where id=%s'
                cursor.execute(sql,(pwd if pwd !='' else row['pwd'], email if email != '' else row['email'],self.id))
            except:
                print('수정에 실패하였습니다.\n')
            else:
                conn.commit()
                print('수정 완료되었습니다.\n')
            finally:
                self.updateInfo()
        elif selectMode == '2':
            ck = input('정말로 삭제하시겠습니까?[y/n] : ')
            if ck.lower()=='y':
                try:
                    sql = 'delete from member where id=\''+self.id+"'"
                    cursor.execute(sql)
                except:
                    print('삭제에 실패하였습니다\n')
                    self.updateInfo()
                else:
                    conn.commit()
                    print('삭제 완료하였습니다.\n')
                    module()

        elif selectMode == '3':
            self.userPage()
        else:
            print('메뉴를 확인해주세요\n')
            self.updateInfo()

    #구매가능한 물품을 조회하기 위한 함수
    def searchItem(self):
        item = input('원하는 상품명을 입력하세요 : ')
        sql = "select product_name,product_price,product_qty from item where product_name ='"+item+"' and product_qty>0"
        cursor.execute(sql)
        rows = cursor.fetchall()
        if len(rows)==0:
            self.itemList()
            print('다시한번 확인하시기 바랍니다.\n')
        else:
            print('{:<10}\t{:<10}\t{:<5}'.format('상품명','가격','수량'))
            for row in rows:
                print('{:<10}\t{:<10,}\t{:<5,}'.format(row['product_name'],row['product_price'],row['product_qty']))
        self.userPage()

    #물품 구매 함수
    def buyList(self):
        self.itemList()        
        item = input("원하는 상품을 입력하세요 : ")
        sql = 'select * from item where product_name=%s'
        cursor.execute(sql,(item))
        row = cursor.fetchone()
        if len(row) != 0:
            try:
                count = input('구매할 제품의 수량을 입력하세요({}이하) : '.format(row['product_qty']))
                if int(count)>row['product_qty']:
                    print('재고보다 많은양은 주문이 불가능합니다.\n')
                    self.buyList()
                sql = 'update item set product_qty=product_qty-%s where product_name=%s;'
                cursor.execute(sql,(count,item))
            except:
                print('구매에 실패하였습니다.\n')
            else:
                try:
                    sql = 'insert into orders(member_id,item_id,item_name,order_qty,order_price,created_at) values(%s,%s,%s,%s,%s,now())'
                    tmp = cursor.execute(sql,(self.id,str(row['id']),item,count,str(int(row['product_price'])*int(count))))
                    print(tmp)
                except:
                    print('구매에 실패하였습니다.\n')
                else:
                    conn.commit()
            finally:
                self.userPage()
        else:
            print('다시한번 확인해주세요\n')
            self.buyList()

    #구매 가능한 상태의 물품 출력
    def itemList(self):
        sql = 'select product_name,product_price,product_qty from item where product_qty>0'
        cursor.execute(sql)
        rows = cursor.fetchall()
        if len(rows) == 0:
	        print('구매 가능할 물건이 없습니다.\n')
	        self.userPage()
        else:
            print('{:<10}\t{:<10}\t{:<5}'.format('상품명','가격','수량'))
            for row in rows:
                print('{:<10}\t{:<10,}\t{:<5,}'.format(row['product_name'],row['product_price'],row['product_qty']))
    
    #로그인한 유저의 주문 내역
    def myOrderList(self):
        sql = 'select item_name,order_price,order_qty,created_at from orders where member_id=%s'
        try:
            cursor.execute(sql,(self.id))
            rows = cursor.fetchall()
            if len(rows) == 0:
                print('주문 내역이 없습니다.')
            else:
                print('{:<10}\t{:<10}\t{:<10}\t{}'.format('제품명','구매 가격','구매 개수','구매 일자'))
                for row in rows:
                    print('{:<10}\t{:<10,}\t{:<10,}\t{}'.format(row['item_name'],row['order_price'],row['order_qty'],row['created_at']))
        except Exception as e:
            print('주문 내역을 불러오는데 실패했습니다.',e)
        finally:
            self.userPage()

    #유저 클래스의 메인함수
    def userPage(self):
        print('1. 회원 정보 수정')
        print('2. 상품 조회')
        print('3. 상품 주문')
        print('4. 주문 내역 조회')
        print('5. 로그아웃')
        
        selectMenu = input('메뉴를 선택하세요 : ')

        if selectMenu == '1':
            self.updateInfo()
        elif selectMenu == '2':
            self.searchItem()
        elif selectMenu == '3':
            self.buyList()
        elif selectMenu == '4':
            self.myOrderList()
        elif selectMenu == '5':
            module()
        else:
            print('메뉴를 화인해주세요.\n')
            self.userPage()

#클래스 실행
if __name__ == '__main__':
    module()
