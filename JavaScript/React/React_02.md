### 댓글 컴포넌트 제작

댓슬을 작성한 작성자의 이미지, 작성자의 이름, 댓글 내용을 출력하는 컴포넌트를 제작

**comment 폴더를 생성하고, Commet.js 파일을 추가**

src/comment/Comment.js

```jsx
function Comment (props) {
    return (
        <>
            <h1>댓글 컴포넌트</h1>
        </>
    );
}

export default Comment;
```

**comment폴더에 CommentList.js 파일을 추가**

src/comment/CommentList.js

```jsx
import Commnet from "./Comment";

function CommentList(props) {
    return (
        <>
            <Commnet/>
            <Commnet/>
            <Commnet/>
        
        </>
    );
}

export default CommentList;
```

**App.js 파일에 CommentList 컴포넌트를 추가**

```jsx
import './App.css';
import CommentList from './comment/CommentList';

function App() {
  return (
    <>
      <CommentList/>
    </>  
  );
}

export default App;
```

**Comment컴포넌트에 작성한 사람의 이미지, 이름, 댓글 내용을 보여주는 코드를 추가**

[사람 이미지](https://upload.wikimedia.org/wikipedia/commons/8/89/Portrait_Placeholder.png)

```jsx
function Comment (props) {
    return (
        <div>
            <div>
                <img src="https://upload.wikimedia.org/wikipedia/commons/8/89/Portrait_Placeholder.png" />
            </div>

            <div>
                <span>작성자 이름</span>
                <span>댓글 내용</span>
            </div>
        </div>
    );
}

export default Comment;
```

**Comment 컴포넌트에 스타일을 추가**

```jsx
function Comment (props) {
    const styles = {
        wrapper: {
            display: 'flex',
            flexDirection: 'row',
            border: '2px solid gray',
            borderRadius: 16,
            padding: 8,
            margin: 8
        }, 
        image: {
            width: 50,
            height: 50,
            borderRadius: 25
        },
        contentContainer: {
            marginLeft: 10,
            display: 'flex',
            flexDirection: 'column'
        },
        nameText: {
            color: 'black',
            fontSize: 16,
            fontWeight: 'bold',
            marginBottom: 5
        },
        commentText: {
            color: 'black',
            fontSize: 16
        }
    }
    return (
        <div style={styles.wrapper}>
            <div>
                <img style={styles.image} src="https://upload.wikimedia.org/wikipedia/commons/8/89/Portrait_Placeholder.png" />
            </div>

            <div style={styles.contentContainer}>
                <span style={styles.nameText}>작성자 이름</span>
                <span style={styles.commentText}>댓글 내용</span>
            </div>
        </div>
    );
}

export default Comment;
```

**Comment컴포넌트에 props변수로 전달된 값을 출력하도록 변경**

Comment.js

```jsx
function Comment (props) {
    const styles = {
        wrapper: {
            display: 'flex',
            flexDirection: 'row',
            border: '2px solid gray',
            borderRadius: 16,
            padding: 8,
            margin: 8
        }, 
        image: {
            width: 50,
            height: 50,
            borderRadius: 25
        },
        contentContainer: {
            marginLeft: 10,
            display: 'flex',
            flexDirection: 'column'
        },
        nameText: {
            color: 'black',
            fontSize: 16,
            fontWeight: 'bold',
            marginBottom: 5
        },
        commentText: {
            color: 'black',
            fontSize: 16
        }
    }
    return (
        <div style={styles.wrapper}>
            <div>
                <img style={styles.image} src="https://upload.wikimedia.org/wikipedia/commons/8/89/Portrait_Placeholder.png" />
            </div>

            <div style={styles.contentContainer}>
                <span style={styles.nameText}>{props.name}</span>
                <span style={styles.commentText}>{props.comment}</span>
            </div>
        </div>
    );
}

export default Comment;
```

CommentList.js

```jsx
import Commnet from "./Comment";

function CommentList(props) {
    return (
        <>
            <Commnet name='홍길동' comment='안녕하세요. 홍길동입니다.'/>
            <Commnet name='고길동' comment='안녕하세요. 둘리가 싫어요.'/>
            <Commnet name='신길동' comment='안녕하세요. 매운짬뽕입니다.'/>
        
        </>
    );
}

export default CommentList;
```

**CommentList 파일에 댓글 데이터를 이용해 Comment가 출력되도록 수정**

```jsx
import Commnet from "./Comment";

function CommentList(props) {
    const comments = [
        { name: '홍길동', comment:'안녕하세요. 홍길동입니다.'},
        { name: '고길동', comment:'안녕하세요. 둘리가 싫어요.'},
        { name: '신길동', comment:'안녕하세요. 매운짬뽕입니다..'},

    ];
    return (
        <>
           {
            comments.map(comment => <Commnet name={comment.name} comment={comment.comment}/>)
           }
        
        </>
    );
}

export default CommentList;
```

**key가 누락되었을 때 경고**

```jsx
import Commnet from "./Comment";

function CommentList(props) {
    const comments = [
        { name: '홍길동', comment:'안녕하세요. 홍길동입니다.'},
        { name: '고길동', comment:'안녕하세요. 둘리가 싫어요.'},
        { name: '신길동', comment:'안녕하세요. 매운짬뽕입니다..'},

    ];
    return (
        <>
           {
            comments.map((comment, index) => <Commnet key = {index} name={comment.name} comment={comment.comment}/>)
           }
        
        </>
    );
}

export default CommentList;
```

- LAB1. 글쓴이 별로 이미지를 다르게 출력하도록 수정
    
    CommentList.js
    
    ```jsx
    import Commnet from "./Comment";
    
    function CommentList(props) {
        const comments = [
            { name: '홍길동', comment:'안녕하세요. 홍길동입니다.', image:"https://png.pngtree.com/png-clipart/20190705/original/pngtree-vector-business-men-icon-png-image_4186858.jpg"},
            { name: '고길동', comment:'안녕하세요. 둘리가 싫어요.', image: "https://png.pngtree.com/png-clipart/20190630/original/pngtree-vector-avatar-icon-png-image_4162757.jpg"},
            { name: '신길동', comment:'안녕하세요. 매운짬뽕입니다.', image: "https://png.pngtree.com/png-clipart/20190520/original/pngtree-male-worker-icon-graphic-png-image_3668949.jpg"},
    
        ];
        return (
            <>
               {
                comments.map((comment, index) => <Commnet key = {index} image={comment.image} name={comment.name} comment={comment.comment}/>)
               }
            
            </>
        );
    }
    
    export default CommentList;
    ```
    
    Comment.js
    
    ```jsx
    function Comment (props) {
        const styles = {
            wrapper: {
                display: 'flex',
                flexDirection: 'row',
                border: '2px solid gray',
                borderRadius: 16,
                padding: 8,
                margin: 8
            }, 
            image: {
                width: 50,
                height: 50,
                borderRadius: 25
            },
            contentContainer: {
                marginLeft: 10,
                display: 'flex',
                flexDirection: 'column'
            },
            nameText: {
                color: 'black',
                fontSize: 16,
                fontWeight: 'bold',
                marginBottom: 5
            },
            commentText: {
                color: 'black',
                fontSize: 16
            }
        }
        return (
            <div style={styles.wrapper}>
                <div>
                    <img style={styles.image} src={props.image} />
                </div>
    
                <div style={styles.contentContainer}>
                    <span style={styles.nameText}>{props.name}</span>
                    <span style={styles.commentText}>{props.comment}</span>
                </div>
            </div>
        );
    }
    
    export default Comment;
    ```
    
- LAB2. 홍길동만 출력되도록 수정
    
    if문 - CommentList.js
    
    ```jsx
    import Commnet from "./Comment";
    
    function CommentList(props) {
        const comments = [
            { name: '홍길동', comment:'안녕하세요. 홍길동입니다.', image:"https://png.pngtree.com/png-clipart/20190705/original/pngtree-vector-business-men-icon-png-image_4186858.jpg"},
            { name: '고길동', comment:'안녕하세요. 둘리가 싫어요.', image: "https://png.pngtree.com/png-clipart/20190630/original/pngtree-vector-avatar-icon-png-image_4162757.jpg"},
            { name: '신길동', comment:'안녕하세요. 매운짬뽕입니다.', image: "https://png.pngtree.com/png-clipart/20190520/original/pngtree-male-worker-icon-graphic-png-image_3668949.jpg"},
    
        ];
        return (
            <>
                <h1>모두 출력</h1>
               {
                comments.map((comment, index) => <Commnet key = {index} image={comment.image} name={comment.name} comment={comment.comment}/>)
               }
               <h1>홍길동만 출력</h1>
               {
                comments.map((comment, index) => {
                    if (comment.name == '홍길동') {
                        return <Commnet key = {index} image={comment.image} name={comment.name} comment={comment.comment}/>}
                    } 
                )}
            </>
        );
    }
    
    export default CommentList;
    ```
    
    filter - CommentList.js
    
    ```jsx
    import Commnet from "./Comment";
    
    function CommentList(props) {
        const comments = [
            { name: '홍길동', comment:'안녕하세요. 홍길동입니다.', image:"https://png.pngtree.com/png-clipart/20190705/original/pngtree-vector-business-men-icon-png-image_4186858.jpg"},
            { name: '고길동', comment:'안녕하세요. 둘리가 싫어요.', image: "https://png.pngtree.com/png-clipart/20190630/original/pngtree-vector-avatar-icon-png-image_4162757.jpg"},
            { name: '신길동', comment:'안녕하세요. 매운짬뽕입니다.', image: "https://png.pngtree.com/png-clipart/20190520/original/pngtree-male-worker-icon-graphic-png-image_3668949.jpg"},
    
        ];
        return (
            <>
                <h1>모두 출력</h1>
               {
                comments.map((comment, index) => <Commnet key = {index} image={comment.image} name={comment.name} comment={comment.comment}/>)
               }
               <h1>홍길동만 출력</h1>
                {
                    comments.filter(comment => comment.name == '홍길동').map((comment, index) => <Commnet key = {index} image={comment.image} name={comment.name} comment={comment.comment}/>)
                }
    
            </>
        );
    }
    
    export default CommentList;
    ```
    
- LAB3. 댓글 정보와 사용자 정보가 분리되어 있는 경우
    
    ```jsx
    import Commnet from "./Comment";
    
    function CommentList(props) {
        // 댓글 데이터
    const comments = [
        { name: "홍길동", comment: "안녕하세요. 홍길동입니다." },
        { name: "신길동", comment: "안녕하세요. 매운 짬뽕입니다." },
        { name: "고길동", comment: "둘리가 싫어요." }
    ];
    
    // 사용자 정보
    const users = [
        { name: "홍길동", image: "https://png.pngtree.com/png-clipart/20190705/original/pngtree-vector-business-men-icon-png-image_4186858.jpg" },
        { name: "신길동", image: "https://png.pngtree.com/png-clipart/20190630/original/pngtree-vector-avatar-icon-png-image_4162757.jpg" },
        { name: "고길동", image: "https://png.pngtree.com/png-clipart/20190520/original/pngtree-male-worker-icon-graphic-png-image_3668949.jpg" }
    ];
    
    const commentsAndUsers = comments.map(c => ({ ...c, image: users.filter(u => u.name === c.name)[0].image }));
    
        return (
            <>
                <h1>모두 출력</h1>
               {
                commentsAndUsers.map((comment, index) => <Commnet key = {index} image={comment.image} name={comment.name} comment={comment.comment}/>)
               }
               
    
            </>
        );
    }
    
    export default CommentList;
    ```
    
- LAB4. 사용자 정보에 주민번호가 전달되었을 때 남, 여 구문을 이름 뒤에 출력하도록 수정해 보세요. 예: 홍길동 (남)