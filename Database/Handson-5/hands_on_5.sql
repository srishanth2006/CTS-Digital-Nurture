// ===============================
// HANDS-ON 5 : MongoDB
// Document Modelling, CRUD & Aggregation
// ===============================

// Step 60
use college_nosql

// Step 61
db.createCollection("feedback")

// Step 62
db.feedback.insertMany([
{
student_id:1,
course_code:"CS101",
semester:"2022-ODD",
rating:4,
comments:"Excellent teaching",
tags:["challenging","well-structured","good-examples"],
submitted_at:new Date("2022-11-30T10:15:00Z"),
attachments:[
{filename:"notes.pdf",size_kb:240}
]
},
{
student_id:2,
course_code:"CS101",
semester:"2022-ODD",
rating:5,
comments:"Very informative",
tags:["challenging","interactive"],
submitted_at:new Date("2022-11-29T09:30:00Z"),
attachments:[
{filename:"slides.pdf",size_kb:180}
]
},
{
student_id:3,
course_code:"CS101",
semester:"2022-ODD",
rating:3,
comments:"Needs more examples",
tags:["challenging"],
submitted_at:new Date("2022-11-28T08:00:00Z")
},
{
student_id:4,
course_code:"CS102",
semester:"2022-ODD",
rating:5,
comments:"Excellent DBMS course",
tags:["interesting","practical"],
submitted_at:new Date("2022-11-27T10:00:00Z"),
attachments:[
{filename:"dbms.pdf",size_kb:300}
]
},
{
student_id:5,
course_code:"CS102",
semester:"2022-ODD",
rating:2,
comments:"Too fast",
tags:["fast"],
submitted_at:new Date("2022-11-26T10:00:00Z")
},
{
student_id:6,
course_code:"CS102",
semester:"2022-ODD",
rating:4,
comments:"Good examples",
tags:["examples","interactive"],
submitted_at:new Date("2022-11-25T10:00:00Z")
},
{
student_id:7,
course_code:"CS103",
semester:"2022-ODD",
rating:5,
comments:"Loved OOP",
tags:["coding","practical"],
submitted_at:new Date("2022-11-24T10:00:00Z")
},
{
student_id:8,
course_code:"CS103",
semester:"2022-ODD",
rating:3,
comments:"Average",
tags:["coding"],
submitted_at:new Date("2022-11-23T10:00:00Z")
},
{
student_id:9,
course_code:"EC101",
semester:"2021-EVEN",
rating:2,
comments:"Needs improvement",
tags:["difficult"],
submitted_at:new Date("2022-11-22T10:00:00Z")
},
{
student_id:10,
course_code:"ME101",
semester:"2022-ODD",
rating:4,
comments:"Very good",
tags:["interesting"],
submitted_at:new Date("2022-11-21T10:00:00Z")
}
])

// Step 64
db.feedback.countDocuments()

// ===============================
// Task 2 - CRUD
// ===============================

// Step 65
db.feedback.find({rating:5})

// Step 66
db.feedback.find({
course_code:"CS101",
tags:"challenging"
})

// Step 67
db.feedback.find(
{},
{
student_id:1,
course_code:1,
rating:1,
_id:0
}
)

// Step 68
db.feedback.updateMany(
{rating:{$lt:3}},
{$set:{needs_review:true}}
)

// Step 69
db.feedback.updateMany(
{needs_review:true},
{$push:{tags:"reviewed"}}
)

// Step 70
db.feedback.deleteMany({
semester:"2021-EVEN"
})

// ===============================
// Task 3 - Aggregation Pipeline
// ===============================

// Step 71
db.feedback.aggregate([
{
$match:{
semester:"2022-ODD"
}
},
{
$group:{
_id:"$course_code",
average_rating:{
$avg:"$rating"
},
feedback_count:{
$sum:1
}
}
},
{
$sort:{
average_rating:-1
}
}
])

// Step 72
db.feedback.aggregate([
{
$match:{
semester:"2022-ODD"
}
},
{
$group:{
_id:"$course_code",
average_rating:{
$avg:"$rating"
},
feedback_count:{
$sum:1
}
}
},
{
$project:{
_id:0,
course_code:"$_id",
average_rating:{
$round:["$average_rating",1]
},
feedback_count:1
}
}
])

// Step 73
db.feedback.aggregate([
{
$unwind:"$tags"
},
{
$group:{
_id:"$tags",
count:{
$sum:1
}
}
},
{
$sort:{
count:-1
}
}
])

// Step 74
db.feedback.createIndex({
course_code:1
})

db.feedback.getIndexes()