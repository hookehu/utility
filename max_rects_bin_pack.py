#-*- coding:utf-8 -*-
import dircache, os, math, sys
from PIL import Image
from psd_tools import PSDImage
from psd_tools import Group
import json

class Rectangle:
		x = 0
		y = 0
		width = 0
		height = 0
		offX = 0
		offY = 0
		origin_width = 0
		origin_height = 0
		arena = 0
		
		def __init__(self):
			self.name = ""
			pass
			
		def clone(self):
			rst = Rectangle()
			rst.name = self.name
			rst.x = self.x
			rst.y = self.y
			rst.width = self.width
			rst.height = self.height
			rst.arena = self.arena
			rst.offX = self.offX
			rst.offY = self.offY
			rst.origin_width = self.origin_width
			rst.origin_height = self.origin_height
			return rst
			
		def to_dict(self):
				rst = {}
				rst['x'] = self.x
				rst['y'] = self.y
				rst['w'] = self.width
				rst['h'] = self.height
				rst['offX'] = self.offX
				rst['offY'] = self.offY
				rst['sourceW'] = self.origin_width
				rst['sourceH'] = self.origin_height
				return rst
			
class FreeRectangleChoiceHeuristic:
		BestShortSideFit = 0 #< -BSSF: Positions the Rectangle against the short side of a free Rectangle into which it fits the best.
		BestLongSideFit = 1 #< -BLSF: Positions the Rectangle against the long side of a free Rectangle into which it fits the best.
		BestAreaFit = 2 #< -BAF: Positions the Rectangle into the smallest free Rectangle into which it fits.
		BottomLeftRule = 3 #< -BL: Does the Tetris placement.
		ContactPointRule = 4 #< -CP: Choosest the placement where the Rectangle touches other Rectangles as much as possible.

			
class MaxRectsBinPack:
		binWidth = 0
		binHeight = 0
		allowRotations = False
		
		usedRectangles = [] #new Vector.<Rectangle>();
		freeRectangles = [] #new Vector.<Rectangle>();
		
		score1 = 0
		score2 = 0
		bestShortSideFit = 0
		bestLongSideFit = 0
		
		def __init__(self, width, height, rotations = True):
				self.init(width, height, rotations)
				
				
		def init(self, width, height, rotations = True):
				if( self.count(width) % 1 != 0 or self.count(height) % 1 != 0):
						print "Must be 2,4,8,16,32,...512,1024,..."
						return
				self.binWidth = width
				self.binHeight = height
				self.allowRotations = rotations
				
				n = Rectangle()
				n.x = 0
				n.y = 0
				n.width = width
				n.height = height
				
				self.usedRectangles = []
				
				self.freeRectangles = []
				self.freeRectangles.append(n)
				
		def count(self, n):
				if( n >= 2 ):
						return self.count(n / 2)
				return n
				 
		def insert(self, rect, method):
				width = rect.width
				height = rect.height
				name = rect.name
				newNode  = Rectangle()
				score1 = 0
				score2 = 0
				if method == FreeRectangleChoiceHeuristic.BestShortSideFit: 
						newNode = self.findPositionForNewNodeBestShortSideFit(width, height)
				elif method == FreeRectangleChoiceHeuristic.BottomLeftRule: 
						newNode = self.findPositionForNewNodeBottomLeft(width, height, score1, score2)
				elif method == FreeRectangleChoiceHeuristic.ContactPointRule: 
						newNode = self.findPositionForNewNodeContactPoint(width, height, score1)
				elif method == FreeRectangleChoiceHeuristic.BestLongSideFit: 
						newNode = self.findPositionForNewNodeBestLongSideFit(width, height, score2, score1)
				elif method == FreeRectangleChoiceHeuristic.BestAreaFit: 
						newNode = self.findPositionForNewNodeBestAreaFit(width, height, score1, score2)
				newNode.name = name
				newNode.offX = rect.offX
				newNode.offY = rect.offY
				newNode.origin_width = rect.origin_width
				newNode.origin_height = rect.origin_height
				newNode.arena = rect.arena
				if newNode.height == 0:
						print "not posi for set"
						return newNode
				
				self.placeRectangle(newNode)
				return newNode
				
		def insert2(self, Rectangles, dst, method):
				del dst[:] #dst.length = 0;
				while(len(Rectangles) > 0):
						bestScore1 = sys.maxint #int.MAX_VALUE
						bestScore2 = sys.maxint #int.MAX_VALUE
						bestRectangleIndex = -1
						bestNode = Rectangle()
						
						for i in range(len(Rectangles)):
								score1 = 0
								score2 = 0
								newNode = self.scoreRectangle(Rectangles[i].width, Rectangles[i].height, method, score1, score2)
								newNode.name = Rectangles[i].name
								newNode.offX = Rectangles[i].offX
								newNode.offY = Rectangles[i].offY
								newNode.origin_width = Rectangles[i].origin_width
								newNode.origin_height = Rectangles[i].origin_height
								newNode.arena = Rectangles[i].arena
								if score1 < bestScore1 or (score1 == bestScore1 and score2 < bestScore2):
										bestScore1 = score1
										bestScore2 = score2
										bestNode = newNode
										bestRectangleIndex = i
										
						if (bestRectangleIndex == -1):
								return
						
						self.placeRectangle(bestNode)
						del Rectangles[bestRectangleIndex] #Rectangles.splice(bestRectangleIndex,1)
				
		def placeRectangle(self, node):
				numRectanglesToProcess = len(self.freeRectangles)
				i = 0
				while i < numRectanglesToProcess:
						if self.splitFreeNode(self.freeRectangles[i], node):
								del self.freeRectangles[i] #freeRectangles.splice(i,1);
								i = i - 1
								numRectanglesToProcess = numRectanglesToProcess - 1
						i = i + 1
				
				self.pruneFreeList()
				
				self.usedRectangles.append(node)
				
		def scoreRectangle(self, width,  height, method, score1, score2):
				newNode = Rectangle()
				self.score1 = sys.maxint #int.MAX_VALUE;
				self.score2 = sys.maxint #int.MAX_VALUE;
				if method == FreeRectangleChoiceHeuristic.BestShortSideFit: 
						newNode = self.findPositionForNewNodeBestShortSideFit(width, height)
				elif method == FreeRectangleChoiceHeuristic.BottomLeftRule: 
						newNode = self.findPositionForNewNodeBottomLeft(width, height, self.score1, self.score2)
				elif method == FreeRectangleChoiceHeuristic.ContactPointRule: 
						newNode = self.findPositionForNewNodeContactPoint(width, height, self.score1)
						self.score1 = -self.score1;
				elif method == FreeRectangleChoiceHeuristic.BestLongSideFit: 
						newNode = self.findPositionForNewNodeBestLongSideFit(width, height, self.score2, self.score1)
				elif method == FreeRectangleChoiceHeuristic.BestAreaFit: 
						newNode = self.findPositionForNewNodeBestAreaFit(width, height, self.score1, self.score2)
				
				#// Cannot fit the current Rectangle.
				if newNode.height == 0:
						self.score1 = sys.maxint #int.MAX_VALUE;
						self.score2 = sys.maxint #int.MAX_VALUE;
						print "not posi for set"
				
				return newNode
				
		#Computes the ratio of used surface area.
		def occupancy(self):
				usedSurfaceArea = 0
				for rect in self.usedRectangles:
						usedSurfaceArea = usedSurfaceArea + rect.width * rect.height;
				
				return usedSurfaceArea / (self.binWidth * self.binHeight)
						
		def findPositionForNewNodeBottomLeft(self, width, height, bestY, bestX):
				bestNode = Rectangle()
				
				bestY = sys.maxint;
				topSideY = 0
				for rect in self.freeRectangles:#(var i:int = 0; i < freeRectangles.length; i++) {
						if rect.width >= width and rect.height >= height:
								topSideY = rect.y + height
								if topSideY < bestY or (topSideY == bestY and rect.x < bestX):
										bestNode.x = rect.x
										bestNode.y = rect.y
										bestNode.width = width
										bestNode.height = height
										bestY = topSideY
										bestX = rect.x
						if self.allowRotations or rect.width >= height and rect.height >= width:
								topSideY = rect.y + width
								if topSideY < bestY or (topSideY == bestY and rect.x < bestX):
										bestNode.x = rect.x
										bestNode.y = rect.y
										bestNode.width = height
										bestNode.height = width
										bestY = topSideY
										bestX = rect.x
				return bestNode
						
		def findPositionForNewNodeBestShortSideFit(self, width, height):
				bestNode = Rectangle()
				
				self.bestShortSideFit = sys.maxint #int.MAX_VALUE;
				self.bestLongSideFit = self.score2
				leftoverHoriz = 0
				leftoverVert = 0
				shortSideFit = 0
				longSideFit = 0
				
				for rect in self.freeRectangles: #(var i:int = 0; i < freeRectangles.length; i++) {
						if rect.width >= width and rect.height >= height:
								leftoverHoriz = math.fabs(rect.width - width)
								leftoverVert = math.fabs(rect.height - height)
								shortSideFit = min(leftoverHoriz, leftoverVert)
								longSideFit = max(leftoverHoriz, leftoverVert)
								
								if shortSideFit < self.bestShortSideFit or (shortSideFit == self.bestShortSideFit and longSideFit < self.bestLongSideFit):
										bestNode.x = rect.x
										bestNode.y = rect.y
										bestNode.width = width
										bestNode.height = height
										self.bestShortSideFit = shortSideFit
										self.bestLongSideFit = longSideFit
						flippedLeftoverHoriz = 0
						flippedLeftoverVert = 0
						flippedShortSideFit = 0
						flippedLongSideFit = 0
						if self.allowRotations and rect.width >= height and rect.height >= width:
								flippedLeftoverHoriz = math.fabs(rect.width - height)
								flippedLeftoverVert = math.fabs(rect.height - width)
								flippedShortSideFit = min(flippedLeftoverHoriz, flippedLeftoverVert)
								flippedLongSideFit = max(flippedLeftoverHoriz, flippedLeftoverVert)
								
								if flippedShortSideFit < self.bestShortSideFit or (flippedShortSideFit == self.bestShortSideFit or flippedLongSideFit < self.bestLongSideFit):
										bestNode.x = rect.x
										bestNode.y = rect.y
										bestNode.width = height
										bestNode.height = width
										self.bestShortSideFit = flippedShortSideFit
										self.bestLongSideFit = flippedLongSideFit
				
				return bestNode
				
		def findPositionForNewNodeBestLongSideFit(self, width, height, bestShortSideFit, bestLongSideFit):
				bestNode = Rectangle()
				self.bestLongSideFit = sys.maxint #int.MAX_VALUE;
				
				leftoverHoriz = 0
				leftoverVert = 0
				shortSideFit = 0
				longSideFit = 0
				for rect in self.freeRectangles: #(var i:int = 0; i < freeRectangles.length; i++) {
						if rect.width >= width and rect.height >= height:
								leftoverHoriz = math.fabs(rect.width - width)
								leftoverVert = math.fabs(rect.height - height)
								shortSideFit = min(leftoverHoriz, leftoverVert)
								longSideFit = max(leftoverHoriz, leftoverVert)
								
								if longSideFit < self.bestLongSideFit or (longSideFit == self.bestLongSideFit and shortSideFit < self.bestShortSideFit):
										bestNode.x = rect.x
										bestNode.y = rect.y
										bestNode.width = width
										bestNode.height = height
										self.bestShortSideFit = shortSideFit
										self.bestLongSideFit = longSideFit
						
						if self.allowRotations and rect.width >= height and rect.height >= width:
								leftoverHoriz = math.fabs(rect.width - height)
								leftoverVert = math.fabs(rect.height - width)
								shortSideFit = min(leftoverHoriz, leftoverVert)
								longSideFit = max(leftoverHoriz, leftoverVert)
								
								if longSideFit < self.bestLongSideFit or (longSideFit == self.bestLongSideFit and shortSideFit < self.bestShortSideFit):
										bestNode.x = rect.x
										bestNode.y = rect.y
										bestNode.width = height
										bestNode.height = width
										self.bestShortSideFit = shortSideFit
										self.bestLongSideFit = longSideFit
				return bestNode
				
		def findPositionForNewNodeBestAreaFit(self, width, height, bestAreaFit, bestShortSideFit):
				bestNode = Rectangle()
				self.bestAreaFit = sys.maxint #int.MAX_VALUE;
				
				leftoverHoriz = 0
				leftoverVert = 0
				shortSideFit = 0
				areaFit = 0
				
				for rect in self.freeRectangles: #(var i:int = 0; i < freeRectangles.length; i++) {
						areaFit = rect.width * rect.height - width * height
						
						if rect.width >= width and rect.height >= height:
								leftoverHoriz = math.fabs(rect.width - width)
								leftoverVert = math.fabs(rect.height - height)
								shortSideFit = min(leftoverHoriz, leftoverVert)
								
								if areaFit < self.bestAreaFit or (areaFit == self.bestAreaFit and shortSideFit < self.bestShortSideFit):
										bestNode.x = rect.x
										bestNode.y = rect.y
										bestNode.width = width
										bestNode.height = height
										self.bestShortSideFit = shortSideFit
										self.bestAreaFit = areaFit
						
						if self.allowRotations and rect.width >= height and rect.height >= width:
								leftoverHoriz = math.fabs(rect.width - height)
								leftoverVert = math.fabs(rect.height - width)
								shortSideFit = min(leftoverHoriz, leftoverVert)
								
								if areaFit < bestAreaFit or (areaFit == self.bestAreaFit and shortSideFit < self.bestShortSideFit):
										bestNode.x = rect.x
										bestNode.y = rect.y
										bestNode.width = height
										bestNode.height = width
										self.bestShortSideFit = shortSideFit
										self.bestAreaFit = areaFit
				return bestNode
				
		def commonIntervalLength(self, i1start, i1end, i2start, i2end):
				if i1end < i2start or i2end < i1start:
						return 0
				return min(i1end, i2end) - max(i1start, i2start)
				
		def contactPointScoreNode(self, x, y, width, height):
				score = 0
				
				if (x == 0 or x + width == self.binWidth):
						score += height
				if (y == 0 or y + height == self.binHeight):
						score += width
				for rect in self.usedRectangles: #(var i:int = 0; i < usedRectangles.length; i++) {
						if (rect.x == x + width or rect.x + rect.width == x):
								score = score + self.commonIntervalLength(rect.y, rect.y + rect.height, y, y + height)
						if (rect.y == y + height or rect.y + rect.height == y):
								score = score + self.commonIntervalLength(rect.x, rect.x + rect.width, x, x + width)
				
				return score
				
		def findPositionForNewNodeContactPoint(self, width, height, bestContactScore):
				bestNode = Rectangle()
				
				bestContactScore = -1
				score = 0
				for rect in self.freeRectangles: #(var i:int = 0; i < freeRectangles.length; i++) {
						if (rect.width >= width and rect.height >= height):
								score = self.contactPointScoreNode(rect.x, rect.y, width, height)
								if (score > bestContactScore):
										bestNode.x = rect.x
										bestNode.y = rect.y
										bestNode.width = width
										bestNode.height = height
										bestContactScore = score
						if (self.allowRotations and rect.width >= height and rect.height >= width):
								score = self.contactPointScoreNode(rect.x, rect.y, height, width)
								if (score > bestContactScore):
										bestNode.x = rect.x
										bestNode.y = rect.y
										bestNode.width = height
										bestNode.height = width
										bestContactScore = score
				return bestNode
				
		def splitFreeNode(self, freeNode, usedNode):
				if (usedNode.x >= freeNode.x + freeNode.width or usedNode.x + usedNode.width <= freeNode.x or
						usedNode.y >= freeNode.y + freeNode.height or usedNode.y + usedNode.height <= freeNode.y):
						return False
				newNode = None
				if (usedNode.x < freeNode.x + freeNode.width and usedNode.x + usedNode.width > freeNode.x):
						if (usedNode.y > freeNode.y and usedNode.y < freeNode.y + freeNode.height):
								newNode = freeNode.clone()
								newNode.height = usedNode.y - newNode.y
								self.freeRectangles.append(newNode)
						
						if (usedNode.y + usedNode.height < freeNode.y + freeNode.height):
								newNode = freeNode.clone()
								newNode.y = usedNode.y + usedNode.height
								newNode.height = freeNode.y + freeNode.height - (usedNode.y + usedNode.height)
								self.freeRectangles.append(newNode)
				
				if (usedNode.y < freeNode.y + freeNode.height and usedNode.y + usedNode.height > freeNode.y):
						if (usedNode.x > freeNode.x and usedNode.x < freeNode.x + freeNode.width):
								newNode = freeNode.clone()
								newNode.width = usedNode.x - newNode.x
								self.freeRectangles.append(newNode)
						
						if (usedNode.x + usedNode.width < freeNode.x + freeNode.width):
								newNode = freeNode.clone()
								newNode.x = usedNode.x + usedNode.width
								newNode.width = freeNode.x + freeNode.width - (usedNode.x + usedNode.width)
								self.freeRectangles.append(newNode)
				
				return True
				
		def pruneFreeList(self):
				i = 0
				j = 0
				flen = len(self.freeRectangles)
				while i < flen:
						j = i + 1
						while j < len(self.freeRectangles):
								if (self.isContainedIn(self.freeRectangles[i], self.freeRectangles[j])):
										del self.freeRectangles[i] #.splice(i,1);
										break
								if (self.isContainedIn(self.freeRectangles[j], self.freeRectangles[i])):
										del self.freeRectangles[j] #.splice(j,1);
								j = j + 1
						i = i + 1
				
		def isContainedIn(self, a, b):
				return a.x >= b.x and a.y >= b.y and\
						 a.x+a.width <= b.x+b.width and\
						 a.y+a.height <= b.y+b.height
						 
class Demo:
		#原图目录
		res_path = "E:/Temp/abc"
		#生成的图集存放目录
		output_path = "E:/Temp"
		total_arena = 0
		MAX_SIZE = 1024
		MIN_SIZE = 128
		BASE_ALPHA = 15
		width = 128
		height = 128
		count = 0
		
		def __init__(self):
				pass
				
		def get_output_name(self):
				name = 'sheet' + str(self.count) + '.png'
				jsonname = 'sheet' + str(self.count) + '.json'
				self.count = self.count + 1
				return name, jsonname
				
		def proc(self):
				files = dircache.listdir(self.res_path)
				self.maxRect = MaxRectsBinPack(self.width, self.height, False)
				rects = []
				self.maps = {}
				for f in files:
						p = self.res_path + '/' + f
						img = Image.open(p)
						img_width, img_height = img.size
						minx, maxx, miny, maxy = self.get_edge(img)
						rw = maxx - minx
						rh = maxy - miny
						img.close()
						self.total_arena = self.total_arena + img_width * img_height
						rect = Rectangle()
						rect.name = f
						rect.origin_width = img_width
						rect.origin_height = img_height
						rect.offX = minx
						rect.offY = miny
						rect.width = rw
						rect.height = rh
						rect.arena = rw * rh
						if rw > 450 or rh > 450:#超过尺寸不打图集
								continue
						rects.append(rect)
						self.maps[f] = p
				rects = sorted(rects, key=lambda s:s.arena)
				while True:
						rst = self.proc_rects(rects)
						if rst:#处理完成
								break
						if self.width == self.height and self.width == self.MAX_SIZE:
								print "next sheet"
								self.output()
								self.width = self.MIN_SIZE
								self.height = self.MIN_SIZE
								continue
						if self.width == self.height:
								self.get_next_width()
								self.maxRect = MaxRectsBinPack(self.width, self.height, False)
								continue
						else:
								self.get_next_height()
								self.maxRect = MaxRectsBinPack(self.width, self.height, False)
								continue
				self.output()
				
		def output(self):
				oi = Image.new("RGBA", (self.width, self.height), 0)
				print self.width, self.height
				od = {}
				od['frames'] = {}
				for r in self.maxRect.usedRectangles:
						i = Image.open(self.maps[r.name])
						crop = i.crop((r.offX, r.offY, r.width, r.height))
						oi.paste(crop, (r.x, r.y))
						i.close()
						od['frames'][r.name.replace('.', '_')] = r.to_dict()
				oimg_name, ojson_name = self.get_output_name()
				oi.save(self.output_path + "/" + oimg_name)
				od["file"] = oimg_name
				jsonstr = json.dumps(od, indent=2, encoding="utf-8")
				fd = open(self.output_path + "/" + ojson_name, 'wb')
				fd.write(jsonstr);
				fd.close();
				
		def proc_rects(self, rects):
				dels = []
				for rect in rects:
						dels.append(rect)
						rst = self.maxRect.insert(rect, FreeRectangleChoiceHeuristic.BestLongSideFit);
						if rst.height == 0:
								if self.width == self.height == self.MAX_SIZE:
										#生成下一个sheet
										for d in dels:
												rects.remove(d)
								return False
				return True
				
		def get_next_width(self):
				self.width = self.width * 2
				if self.width > self.MAX_SIZE:
						self.width = self.MAX_SIZE
		
		def get_next_height(self):
				self.height = self.height * 2
				if self.height > self.MAX_SIZE:
						self.height = self.MAX_SIZE
						
		def get_edge(self, img):
				alpha = img.load()
				w, h = img.size
				minx = 0
				maxx = w
				miny = 0
				maxy = h
				x = 0
				find = False
				while x < w:
						y = 0
						while y < h:
								p = alpha[x, y]
								if len(p) <= 3:
										p = (p[0], p[1], p[2], 255)
								if p[3] > self.BASE_ALPHA:
										minx = x
										find = True
										break
								y = y + 1
						if find:
								break
						x = x + 1
				find = False
				x = w - 1
				while x >= 0:
						y = 0
						while y < h:
								p = alpha[x, y]
								if len(p) <= 3:
										p = (p[0], p[1], p[2], 255)
								if p[3] > self.BASE_ALPHA:
										maxx = x
										find = True
										break
								y = y + 1
						if find:
								break
						x = x - 1
				find = False
				y = 0
				while y < h:
						x = 0
						while x < w:
								p = alpha[x, y]
								if len(p) <= 3:
										p = (p[0], p[1], p[2], 255)
								if p[3] > self.BASE_ALPHA:
										miny = y
										find = True
										break
								x = x + 1
						if find:
								break
						y = y + 1
				find = False
				y = h - 1
				while y >= 0:
						x = 0
						while x < w:
								p = alpha[x, y]
								if len(p) <= 3:
										p = (p[0], p[1], p[2], 255)
								if p[3] > self.BASE_ALPHA:
										maxy = y
										find = True
										break
								x = x + 1
						if find:
								break
						y = y - 1
				return minx, maxx, miny, maxy
						
		def begin(self):
				files = dircache.listdir(self.res_path)
				maxRect = MaxRectsBinPack(512, 256, False)
				rects = []
				maps = {}
				for f in files:
					p = self.res_path + '/' + f
					img = Image.open(p)
					img_width, img_height = img.size
					self.total_arena = self.total_arena + img_width * img_height
					rect = Rectangle()
					rect.name = f
					rect.width = img_width
					rect.height = img_height
					rects.append(rect)
					maps[f] = img
				maxRect.insert2(rects, [], FreeRectangleChoiceHeuristic.BestLongSideFit)
				oi = Image.new("RGBA", (512, 256), 0)
				for r in maxRect.usedRectangles:
					print str(r.x) + "_" + str(r.y) + "_" + str(r.width) + "_" + str(r.height)
					i = maps[r.name]
					crop = i.crop((0, 0, r.width, r.height))
					oi.paste(crop, (r.x, r.y))
				#oi.show()
				oi.save(self.output_path + "/test.png")
				print self.total_arena
						
if __name__ == "__main__":
	d = Demo()
	d.proc()
	print "success"