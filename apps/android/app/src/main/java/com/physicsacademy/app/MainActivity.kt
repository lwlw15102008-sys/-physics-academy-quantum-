package com.physicsacademy.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

private val Navy = Color(0xFF080D1A)
private val Blue = Color(0xFF3987FF)
private val Cyan = Color(0xFF35D5E8)
private val Dim = Color(0xFF8291AA) // 6:1 contrast on Navy

private val subjects = listOf("الفيزياء", "الكيمياء", "الأحياء", "الرياضيات", "الجيولوجيا")
private val tabs = listOf("الرئيسية", "تعلّم", "المختبرات", "الألعاب", "تقدّمي")

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { PhysicsAcademyApp() }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PhysicsAcademyApp() {
    // Saveable state survives rotation and process death.
    var selectedSubject by rememberSaveable { mutableStateOf<String?>(null) }
    var selectedTab by rememberSaveable { mutableStateOf(tabs.first()) }

    val notice: String? = when {
        selectedSubject != null -> "مادة $selectedSubject: سيتم فتح وحداتها بعد إدخال المنهج وربط الخادم."
        selectedTab != tabs.first() -> "قسم $selectedTab: المحتوى التفاعلي سيتم تفعيله بعد توصيل الخدمات."
        else -> null
    }

    MaterialTheme(colorScheme = darkColorScheme(background = Navy, surface = Color(0xFF111B30), primary = Blue, secondary = Cyan)) {
        // The app is Arabic-first: force right-to-left regardless of device locale.
        CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Rtl) {
            Surface(modifier = Modifier.fillMaxSize(), color = Navy) {
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(Brush.linearGradient(listOf(Navy, Color(0xFF142544), Navy)))
                        .verticalScroll(rememberScrollState())
                        .padding(20.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    Text("PHYSICS ACADEMY", color = Cyan, fontSize = 13.sp, fontWeight = FontWeight.Bold)
                    Text("مرحباً بك في عالمك العلمي", color = Color.White, fontSize = 25.sp, fontWeight = FontWeight.ExtraBold)
                    Text("تعلّم بذكاء، جرّب بنفسك، واكتشف قدراتك.", color = Color.LightGray, fontSize = 13.sp)

                    Row(modifier = Modifier.horizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        tabs.forEach { tab ->
                            FilterChip(
                                selected = selectedTab == tab,
                                onClick = { selectedTab = tab; selectedSubject = null },
                                label = { Text(tab) }
                            )
                        }
                    }

                    if (notice != null) Text(notice, color = Cyan, fontSize = 12.sp)

                    Card(colors = CardDefaults.cardColors(containerColor = Color(0xFF17233B)), shape = RoundedCornerShape(22.dp)) {
                        Column(Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                            Text("ابدأ رحلتك", color = Color.White, fontSize = 19.sp, fontWeight = FontWeight.Bold)
                            Text("اختر مادة دراسية لاستعراض مسارها.", color = Color.LightGray, fontSize = 13.sp)
                            Button(onClick = { selectedTab = "تعلّم"; selectedSubject = null }) { Text("استكشف المواد") }
                        }
                    }

                    Text("المواد الدراسية", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 18.sp)
                    subjects.forEach { subject ->
                        val selected = selectedSubject == subject
                        Card(
                            onClick = { selectedSubject = if (selected) null else subject },
                            colors = CardDefaults.cardColors(containerColor = if (selected) Color(0xFF1C355B) else Color(0xFF111B30)),
                            shape = RoundedCornerShape(16.dp)
                        ) {
                            Row(Modifier.fillMaxWidth().padding(15.dp), verticalAlignment = Alignment.CenterVertically) {
                                Text(subject, color = Color.White, modifier = Modifier.weight(1f), fontWeight = if (selected) FontWeight.Bold else FontWeight.Normal)
                                Text(if (selected) "محددة" else "استكشف", color = Cyan, fontSize = 12.sp)
                            }
                        }
                    }

                    Text("نسخة تأسيسية 0.3.0 · لا توجد بيانات حساب محفوظة بعد", color = Dim, fontSize = 11.sp)
                }
            }
        }
    }
}
