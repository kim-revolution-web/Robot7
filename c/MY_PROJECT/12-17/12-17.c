#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h> 
#include <limits.h> 



//studio code로 해서 조금 다름 구조체 배열로 만듬
#define MAX 200
typedef struct
{
    int id;
    char name[20];
    char type[20];
    char location[30];
    int status; 
    char note[100];

} Equipment;
Equipment list[MAX];
int count = 0;
int next_id = 1;

// 입력 안정화
void read_std(char *readstd, size_t size)
{
    int ch = 0;
    int a = 0;

    if (readstd == NULL || size == 0)
    {
        printf("read 입력값이 오지 않음");
        return;
    }
    if (fgets(readstd, size, stdin) == NULL)
    {
        readstd[0] = '\0';
        return;
    }
    int had_newline = (strchr(readstd, '\n') != NULL); // 먼저 체크
    readstd[strcspn(readstd, "\r\n")] = '\0';          // 그 다음 제거

    if (!had_newline)
    {
        int ch;
        while ((ch = getchar()) != '\n' && ch != EOF)
        {
        }
    }
}

int read_int()
{
    char buf[64];
    while (1)
    {
        read_std(buf, sizeof(buf));
        if (buf[0] == '\0')
        {
            printf("빈 입력입니다.");
            continue;
        }

        char *str = NULL;
        errno = 0; // 이거뭐야
        long v = strtol(buf, &str, 10);

    
        if (str == buf)
        {
            printf("정수가 아닙니다. 다시 입력하세요.\n");
            continue;
        }
        if (*str != '\0')
        {
            printf("정수만 입력하세요.\n");
            continue;
        }
        if (errno == ERANGE || v < INT_MIN || v > INT_MAX)
        { //
            printf("정수 범위를 벗어났습니다.\n");
            continue;
        }
        return (int)v;
    }
}

// load_all(char* filename,char *list,int &count,char &next_id)
// {
//     strtok_s();

// }

// save_all(char* filename,char *list,int count){

// }

// add_equipment(list, &count, &next_id)

// find_index_by_id(list, count, id) ← 이게 핵심

// update_equipment(list, count)

// delete_equipment(list, &count)

//---------------------------------------------
void fileREAD()
{

    FILE *fpr=fopen("i.txt", "r");
    if(fpr ==NULL){printf("파일열기 실패"); return;}

    char str[300];
  
    while (fgets(str, sizeof(str), fpr) != NULL)
    {
        str[strcspn(str, "\r\n")] = '\0';
        if(str[0]=='\0')continue;

    if(count>=MAX){printf("MAX 초과\n"); break;}
    Equipment* e =&list[count];
    memset(e,0,sizeof(*e));
        char *tok;
        
        tok=strtok(str,"|");
        if(!tok)continue;
        e->id=(int)strtol(tok,NULL,10);

        tok=strtok(NULL,"|");
        if(!tok)continue;
        strncpy(e->name,tok,sizeof(e->name)-1);

        tok=strtok(NULL,"|");
        if(!tok)continue;
        strncpy(e->type,tok,sizeof(e->type)-1);

        tok=strtok(NULL,"|");
        if(!tok)continue;
        strncpy(e->location,tok,sizeof(e->location)-1);

        tok=strtok(NULL,"|");
        if(!tok)continue;
        e->status=(int)strtol(tok,NULL,10);

        
        tok = strtok(NULL, "|");
        if (!tok) tok = "";                 
        strncpy(e->note, tok, sizeof(e->note)-1); 

        if (e->id >= next_id) next_id = e->id + 1; //id 자동 카운트

        count++;
    }
    fclose(fpr);

}

void case_1()
{
    if(count ==0 ){printf(" 데이터 없음"); return;}
    else{
        for(int i=0;i<count;i++){
            printf("%s",list[i]);
        }
    }

}

void case_2()
{
    if(count >=MAX){printf("입력을 초과했습니다");}

    Equipment e = {0};
    e.id = next_id++;
    printf("이름:");
    read_std(e.name, sizeof(e.name));

    printf("타입:");
    read_std(e.type, sizeof(e.type));

    printf("로케이션?:");
    read_std(e.location, sizeof(e.location));

    printf("상태:");
    int a=0;
    while(!a){
    if(read_int(e.status, sizeof(e.status))==1||
    read_int(e.status, sizeof(e.status))== 0){
        a=1;
    }
    }

    printf("노트:");
    read_std(e.note, sizeof(e.note));

    list[count] =e;
    count++;
    FILE *fpa=fopen("i.txt","a+");
    if(fpa==NULL){printf("case_2에 파일이 열리지 않았습니다."); return;}
    fprintf(fpa,"%d|%s|%s|%s|%d|%s",e.id,e.name,e.type,e.location,e.status,e.note);
}
int main()
{
    fileREAD();
    int choice = 0;
    while (1)
    {

        printf("1.목록");
        printf("2.추가");
        printf("3.수정");
        printf("4.삭제");
        printf("5.저장");
        printf("0.종료");
        printf("선택>");
        choice = read_int();

        switch (choice)
        {
        case 1:
            case_1();
            break;
        case 2:
        case_2();
            break;
        case 3:
            /* code */
            break;
        case 4:
            /* code */
            break;
        case 5:
            /* code */
            break;
        case 0:
            printf("종료");
            return 0;
            /* code */
            break;
        default:
            break;
        }
    }
}
